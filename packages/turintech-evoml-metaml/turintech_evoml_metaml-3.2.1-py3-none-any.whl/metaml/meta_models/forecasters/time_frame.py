from __future__ import annotations
import pandas as pd
import numpy as np
import collections.abc
import warnings

from enum import Enum
from typing import Mapping, Union, Sequence, Optional, List, Hashable, Tuple, Iterable
from functools import reduce

from metaml.exceptions import IndexTypeException

warnings.simplefilter(action="ignore", category=FutureWarning)

IdentifierType = Hashable
"""The type of any element of the identifier columns. Must be hashable to be used as a key in a dictionary."""

StepSizeType = Union[int, pd.DateOffset]
"""The type of the step size of a subseries. Can be either an integer or a pandas DateOffset."""

StepSizeDictType = Mapping[IdentifierType, StepSizeType]
"""A mapping from subseries identifiers to their step sizes."""

DateOffsetAlias = str
"""A string which can be converted to a pandas DateOffset via pd.tseries.frequencies.to_offset."""

StepSizeSuggestionType = Union[StepSizeType, DateOffsetAlias]
"""The types with which a user can suggest a step size which will later be converted to StepSizeType."""

StepSizeSuggestionDictType = Mapping[IdentifierType, StepSizeSuggestionType]
"""A mapping from subseries identifiers to a user suggested step size which will be later converted to StepSizeType."""

IndexType = Union[int, pd.Timestamp]
"""The type of elements in the index column. Currently we don't support a mixture of types in the index."""


class IndexTypeEnum(str, Enum):
    """Enum to represent the type of the index of a time series, which may consist of either datetimes or integers."""

    DATETIME = "datetime"
    INTEGER = "integer"


PLACEHOLDER_ID = "Series0"
"""If we are dealing with a single series and an ID isn't provided then this constant will be used to fill the 
identifier column."""


class TimeFrame:
    """
    TimeFrame is a wrapper around a pandas DataFrame designed to handle multiple time series and track their indexes.
    This class guarantees that any time series it contains will have no missing values and will have an index with a
    known step size. Time series are stored in a narrow format. The index column stores the time to which each row
    corresponds. The identifier columns are used to which series each row belongs to. Multiple columns allow us to store
    a hierarchy of identifiers such as country, region, subregion, etc. The data columns store the actual data for each
    time series.

    Attributes:
        data (pd.DataFrame): DataFrame holding the time series data.
        index_type (IndexTypeEnum): Enum representing the type of index (either datetime or integer).
        step_sizes (Mapping[IdentifierType, StepSizeType]): A dictionary mapping subseries identifiers to
            their respective step sizes.
        index_col (str): The name of the column that serves as the index.
        identifier_cols (List[str]): The columns that are used to identify to which subseries each row belongs.
        zeroth_time_indexes (Mapping[IdentifierType, IndexType]): A dictionary mapping subseries
            identifiers to their respective zeroth time index.
        data_cols (List[str]): The names of the columns that contain data (not including the index and identifier columns).

    """

    data: pd.DataFrame  # DataFrame to hold the time series data
    groupby: pd.core.groupby.DataFrameGroupBy  # Cached groupby object to avoid recomputing when accessing series
    index_type: IndexTypeEnum  # Index data type (either datetime or integer)
    step_sizes: Mapping[IdentifierType, StepSizeType]  # Dictionary to keep track of each subseries' step sizes
    index_col: str  # Name of the column that serves as index
    identifier_cols: List[str]  # Columns that serve to identify to which subseries each row belongs
    zeroth_time_indexes: Mapping[IdentifierType, IndexType]  # Dictionary to keep track of each subseries' zeroth index
    data_cols: List[str]  # Columns that contain data i.e. all columns except index and identifier columns
    series_ids: List[IdentifierType]  # List of all series identifiers

    # Construction methods
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(
        self,
        data: pd.DataFrame,  # Input DataFrame to create TimeFrame
        index_col: str,  # Column to serve as index
        identifier_cols: List[str],  # Columns to identify to which subseries each row belongs
        step_sizes: Optional[
            Union[StepSizeSuggestionDictType, StepSizeSuggestionType]
        ] = None,  # User-suggested frequency to be checked against the actual series
    ):
        self.data = data.copy()  # Create a copy of data to avoid modifying original DataFrame
        self.index_col = index_col  # Store index column name
        self.identifier_cols = identifier_cols  # Store identifier column names
        self.data_cols = [col for col in self.data.columns if col not in [self.index_col] + self.identifier_cols]

        # Validate and preprocess data
        self._validate_and_sort_data()

        # Determine index type (integer or datetime)
        self._determine_index_type()

        # Initialize the dictionary of suggested step sizes
        suggested_step_sizes = self._initialize_suggested_step_sizes(step_sizes)

        # Infer of validate the step sizes of each subseries
        self.step_sizes = self._calculate_step_sizes(suggested_step_sizes)

        # Store first index of each subseries to anchor time series frame of reference
        self.zeroth_time_indexes = self._calculate_zeroth_time_indexes()

    def _validate_and_sort_data(self) -> None:
        """
        Validate and preprocess the input DataFrame data.

        The method performs several operations to ensure the data is correctly formatted for the TimeFrame:
        - Checks that the DataFrame contains the required index and identifier columns.
        - Sorts the DataFrame by identifier and index.
        - Resets the DataFrame index.
        - Reorders the DataFrame columns so that identifier and index columns come first.

        Raises:
            ValueError: If the DataFrame does not contain all the required columns.

        Returns:
            None
        """
        # Check that the DataFrame has the required index and identifier columns
        required_cols = [self.index_col] + self.identifier_cols
        if not set(self.data.columns) >= set(required_cols):
            missing_cols = set(required_cols) - set(self.data.columns)
            raise ValueError(f"DataFrame is missing the following columns: {missing_cols}")

        # Sort the DataFrame by identifier and index
        sort_cols = self.identifier_cols + [self.index_col]
        self.data.sort_values(by=sort_cols, inplace=True)

        # Reset the DataFrame index
        self.data.reset_index(drop=True, inplace=True)

        # Reorder the DataFrame columns
        sorted_cols = sort_cols + sorted([col for col in self.data.columns if col not in sort_cols])
        self.data = self.data.reindex(columns=sorted_cols)

        # After sorting and indexing we can cache a groupby object to group the series
        self.groupby = self.data.groupby(self.identifier_cols)

        # Cache the ids of all series present in the dataset
        self.series_ids = [identifier for identifier, group in self.groupby]

    def _determine_index_type(self) -> None:
        """
        Determine the index type (datetime or integer) of the DataFrame.
        If the index type is neither datetime nor integer, an exception is raised.

        Raises:
            IndexTypeException: If the index type is neither datetime nor integer.
        """
        if pd.api.types.is_datetime64_dtype(self.data[self.index_col]):
            self.index_type = IndexTypeEnum.DATETIME
        elif pd.api.types.is_integer_dtype(self.data[self.index_col]):
            self.index_type = IndexTypeEnum.INTEGER
        else:
            raise IndexTypeException("Index column must be either datetime or integer")

    def _initialize_suggested_step_sizes(
        self, suggested_step_sizes: Optional[Union[StepSizeSuggestionType, StepSizeSuggestionDictType]]
    ) -> StepSizeDictType:
        """
        Initializes the dictionary of suggested step sizes for each subseries based on user input. If no step sizes are
        supplied then this dictionary is empty. If one step size is provided then this is used for all subseries. If
        suggestions take the form of strings then they are converted to pandas offsets.

        Args:
            suggested_step_sizes (Optional[Union[StepSizeSuggestionType, StepSizeSuggestionDictType]]): User-provided
            step sizes, can be either a single step size or a dictionary of step sizes.

        Returns:
            step_sizes: Initialized step size dictionary.
        """
        if suggested_step_sizes is None:
            return {}

        if not isinstance(suggested_step_sizes, dict):
            suggested_step_sizes = {id: suggested_step_sizes for id in self.series_ids}

        suggested_step_sizes = {
            series_id: step_size
            for series_id, step_size in suggested_step_sizes.items()
            if series_id in self.series_ids
        }

        for step_size in suggested_step_sizes.values():
            self._check_step_size_type(step_size)

        suggested_step_sizes = {
            id: pd.tseries.frequencies.to_offset(step_size) if isinstance(step_size, str) else step_size
            for id, step_size in suggested_step_sizes.items()
        }  # Convert strings to pandas offsets if index type is datetime, otherwise leave as is

        return suggested_step_sizes

    def _check_step_size_type(self, step_size: StepSizeSuggestionType):
        if self.index_type == IndexTypeEnum.DATETIME and not isinstance(step_size, (str, pd.DateOffset)):
            raise IndexTypeException(
                f"Suggested step sizes for datetime indices must be either a string or a pandas DateOffset: {step_size}."
            )
        if self.index_type == IndexTypeEnum.INTEGER and not isinstance(step_size, int):
            raise IndexTypeException(f"Suggested step sizes for integer indices must be integers: {step_size}.")

    def _calculate_step_sizes(
        self, suggested_step_sizes: Mapping[IdentifierType, StepSizeType]
    ) -> Mapping[IdentifierType, StepSizeType]:
        """
        Infers the step sizes of any subseries which has no user suggested step size. Checks that any user provided
        step sizes are consistent with the indexes of the corresponding subseries.

        Args:
            suggested_step_sizes: User suggested step sizes.

        Raises:
            IndexError: If the provided step size is not consistent with the indexes of the corresponding subseries.

        Returns:
            step_sizes: Dictionary of step sizes for each subseries.
        """
        step_sizes = {
            uid: self._infer_step_size(uid) if uid not in suggested_step_sizes else suggested_step_sizes[uid]
            for uid in self.series_ids
        }

        if inconsistent_step_sizes := [
            uid for uid, step_size in suggested_step_sizes.items() if not self._is_step_size_consistent(uid, step_size)
        ]:
            raise IndexError(f"Supplied step size is not consistent with subseries: {inconsistent_step_sizes}")

        return step_sizes

    def _infer_step_size(self, identifier: IdentifierType) -> Union[int, pd.DateOffset]:
        """
        Infer the step size of a subseries.

        Args:
            identifier: The identifier of the subseries.

        Raises:
            IndexError: If the step size for the subseries cannot be inferred.

        Returns:
            The inferred step size of the subseries, either as an int or pd.DateOffset.
        """
        group = self.groupby.get_group(identifier)

        if self.index_type == IndexTypeEnum.DATETIME:
            return self._infer_datetime_step_size(group, identifier)
        elif self.index_type == IndexTypeEnum.INTEGER:
            return self._infer_integer_step_size(group, identifier)
        raise IndexTypeException(f"Index type {self.index_type} is not supported.")

    def _infer_datetime_step_size(self, group: pd.DataFrame, identifier: IdentifierType) -> pd.DateOffset:
        """
        Infer the step size of a subseries with a datetime index.

        Args:
            group: The grouped subseries.
            identifier: The identifier of the subseries.

        Raises:
            IndexError: If the datetime step size for the subseries cannot be inferred.

        Returns:
            The inferred datetime step size of the subseries.
        """
        if not (step_size_str := pd.infer_freq(group[self.index_col], warn=True)):
            raise IndexError(f"Could not infer step size of subseries index: {identifier}")
        step_size = pd.tseries.frequencies.to_offset(step_size_str)
        if not isinstance(step_size, pd.DateOffset):
            raise IndexError(f"Could not infer step size of subseries index: {identifier}.")
        return step_size

    def _infer_integer_step_size(self, group: pd.DataFrame, identifier: IdentifierType) -> int:
        """
        Infer the integer step size of a subseries.

        Args:
            group: The grouped subseries.
            identifier: The identifier of the subseries.

        Raises:
            IndexError: If the integer step size for the subseries cannot be inferred.

        Returns:
            The inferred integer step size of the subseries.
        """
        steps = np.unique(np.diff(group[self.index_col].to_numpy()))
        if len(steps) != 1:
            raise IndexError(f"Could not infer step size of subseries index: {identifier}")
        return int(steps[0])

    def _is_step_size_consistent(self, identifier: IdentifierType, step_size: Union[int, pd.DateOffset]) -> bool:
        """
        Check if a supplied step size is consistent with the index of a subseries.

        Args:
            identifier: The identifier of the subseries.
            step_size: The user supplied step size.

        Returns:
            A boolean indicating if the supplied step size is consistent with the index of the subseries.
        """
        group = self.groupby.get_group(identifier)
        time_index = group[self.index_col]

        if self.index_type == IndexTypeEnum.DATETIME:
            reference_index = pd.date_range(start=time_index.iloc[0], freq=step_size, periods=len(time_index))
        elif self.index_type == IndexTypeEnum.INTEGER:
            reference_index = pd.RangeIndex(
                start=time_index.iloc[0], step=step_size, stop=time_index.iloc[0] + len(time_index) * step_size
            )
        else:
            raise IndexTypeException(f"Index type {self.index_type} is not supported.")

        return all(pd.Index(time_index) == reference_index)

    def _calculate_zeroth_time_indexes(self) -> Mapping[IdentifierType, IndexType]:
        """
        Calculate the zeroth value time index for each subseries in the DataFrame.

        It's helpful in anchoring the frame of reference for each time series.

        Returns:
            A dictionary mapping each identifier to its corresponding zeroth time index value.
        """
        return self.groupby[self.index_col].min().to_dict()

    def copy(self):
        """Return a copy of the TimeFrame."""
        return TimeFrame(
            data=self.data,
            index_col=self.index_col,
            identifier_cols=self.identifier_cols,
            step_sizes=self.step_sizes,
        )

    def add_identifier(self, identifier_name: str, identifier_value: IdentifierType) -> TimeFrame:
        data = self.data.copy()
        data[identifier_name] = identifier_value

        step_sizes = {}
        for series_id in self.series_ids:
            if isinstance(series_id, tuple):
                new_id = tuple(list(series_id) + [identifier_value])
            else:
                new_id = (series_id, identifier_value)
            step_sizes[new_id] = self.step_sizes[series_id]

        return TimeFrame(
            data=data,
            index_col=self.index_col,
            identifier_cols=self.identifier_cols + [identifier_name],
            step_sizes=step_sizes,
        )

    def __setitem__(self, column: str, value):
        """
        Sets the values of a specified column.

        Args:
            column (str): The column to be modified.
            value : The value to set for the specified column.
        """
        if column in self.identifier_cols:
            raise ValueError("TimeFrame setter cannot be used to set identifier columns.")
        if column == self.index_col:
            raise ValueError("TimeFrame setter cannot be used to set the index column.")

        self.data.loc[:, column] = value

    @classmethod
    def from_indexed_frame(cls, df: pd.DataFrame) -> TimeFrame:
        # Reset the index to convert MultiIndex to columns
        data = df.reset_index()

        if df.index.nlevels == 1:
            # If there's only a single level in the index, it serves as the index_col
            index_col = df.index.name
            identifier_cols = ["series_id"]

            # Add a new column as the identifier column and set its value to a constant
            data[identifier_cols] = PLACEHOLDER_ID

            # If index is datetime, initialize step_sizes with the index's frequency
            if pd.api.types.is_datetime64_dtype(df.index) and df.index.freq is not None:
                step_sizes = {PLACEHOLDER_ID: df.index.freq}
            else:
                step_sizes = None
        else:
            # Obtain the column names from the MultiIndex
            identifier_cols = df.index.names[:-1]
            index_col = df.index.names[-1]

            # Determine the user-suggested step sizes as None since it will be inferred later
            step_sizes = None

        # Create a TimeFrame object using the extracted identifier, index columns, and the updated DataFrame
        return TimeFrame(
            data=data,
            index_col=index_col,
            identifier_cols=identifier_cols,
            step_sizes=step_sizes,
        )

    def to_indexed_frame(self) -> pd.DataFrame:
        """Return a dataframe with the identifier and index columns stored in a multiindex."""
        return self.data.set_index(self.identifier_cols + [self.index_col])

    # Merge methods
    # ------------------------------------------------------------------------------------------------------------------
    def merge(self, right: Union[pd.DataFrame, TimeFrame]) -> TimeFrame:
        """
        Produce a new TimeFrame by merging a new TimeFrame.

        Args:
            right (TimeFrame): The TimeFrame from which to add data.

        Raises:
            ValueError: If the step sizes of any existing subseries change.

        Returns:
            TimeFrame: The updated TimeFrame.
        """
        if isinstance(right, pd.DataFrame):
            return self.merge_from_frame(right)
        # Retrieve the input TimeFrame's data to a DataFrame and update
        return self.merge_from_frame(right.data, step_sizes=right.step_sizes)

    @classmethod
    def merge_list(cls, time_frames: List[TimeFrame]) -> TimeFrame:
        return reduce(lambda x, y: x.merge(y), time_frames)

    @classmethod
    def concatenate_list(cls, time_frames: List[TimeFrame]) -> TimeFrame:
        """Concatenate a list of TimeFrames into a single TimeFrame. TimeFrames may overlap in time provided the
        overlapping times correspond to different series ids"""

        if not time_frames:
            raise ValueError("time_frames list is empty")

        # Combine step sizes from all TimeFrame objects
        combined_step_sizes = {key: value for tf in time_frames for key, value in tf.step_sizes.items()}

        # Check for conflicts in step sizes
        conflicts = []
        for tf in time_frames:
            for key, value in tf.step_sizes.items():
                if combined_step_sizes[key] != value:
                    conflicts.append(f"{key}: {combined_step_sizes[key]} != {value}")

        if conflicts:
            raise ValueError(f"Conflicts found in step sizes: {', '.join(conflicts)}")

        # Validate that all time frames have the same index_col and identifier_cols
        index_col = time_frames[0].index_col
        identifier_cols = time_frames[0].identifier_cols
        if not all(tf.index_col == index_col and tf.identifier_cols == identifier_cols for tf in time_frames):
            raise ValueError("Not all time frames have the same index_col and identifier_cols")

        # Convert each TimeFrame to a DataFrame and concatenate them
        data_frames = [time_frame.to_indexed_frame() for time_frame in time_frames]
        data = pd.concat(data_frames, axis=0).sort_values(by=identifier_cols + [index_col]).reset_index()

        # Creating a subset with identifier and index columns
        subset = data[identifier_cols + [index_col]]

        # Identifying identical neighboring rows
        identical_neighbors_mask = subset.eq(subset.shift()).all(axis=1)
        # Make sure the mask covers both rows of each pair
        identical_neighbors_mask = identical_neighbors_mask | identical_neighbors_mask.shift(-1)
        if identical_neighbors_mask.any():
            raise ValueError(
                f"Overlapping rows found in the concatenated TimeFrames:\n{data[identical_neighbors_mask]}"
            )

        return cls(data=data, index_col=index_col, identifier_cols=identifier_cols, step_sizes=combined_step_sizes)

    def merge_from_frame(
        self, right: pd.DataFrame, step_sizes: Union[StepSizeSuggestionType, StepSizeSuggestionDictType, None] = None
    ) -> TimeFrame:
        """Produce a new TimeFrame from merged data.

        Args:
            right (pd.DataFrame): The new data to append. Should be a DataFrame with the same structure as the original
                data used to create the TimeFrame.
            step_sizes (Union[StepSizeSuggestionType, StepSizeSuggestionDictType, None]): Step sizes for the new data.

        Raises:
            ValueError: If the step sizes of any existing subseries change.
            KeyError: If any of the identifier columns are missing in new_data.
        """

        if step_sizes is None:
            step_sizes = {}
        self._validate_new_data(new_data=right)
        merged_data = self._merge_data(right=right)

        # Create a new TimeFrame with the updated data
        merged_tsf = TimeFrame(
            merged_data,
            index_col=self.index_col,
            identifier_cols=self.identifier_cols,
            step_sizes={**self.step_sizes, **step_sizes},
        )
        if inconsistent_series := [
            series_id
            for series_id in self.step_sizes
            if series_id in merged_tsf.step_sizes and merged_tsf.step_sizes[series_id] != self.step_sizes[series_id]
        ]:
            raise ValueError(f"The step sizes for the following series do not agree: {inconsistent_series}.")

        # Return the updated TimeFrame
        return merged_tsf

    def _merge_data(self, right: pd.DataFrame) -> pd.DataFrame:
        """
        Merge the new data into the existing data.

        Rows present in both the existing and the new data are aligned on the index and identifier columns. The merge
        strategy used is 'outer' which means all rows from both dataframes are included.

        If a data column exists in both dataframes then they are first suffixed with '_old' (for the existing data) and
        '_new' (for the new data). We then check for conflicts between these two columns and raise an error if any are
        found. The suffixes are then dropped and a single column remains.

        Args:
            right (pd.DataFrame): The new data to merge in. Should be a DataFrame with the same index and identifier
            columns as the existing data.

        Returns:
            pd.DataFrame: The merged dataframe with conflicts resolved.
        """
        # Rows are aligned on the index and identifier columns
        merge_on_cols = [self.index_col] + self.identifier_cols

        # The  "_old" and "_new" suffixes are added to columns that are found in the both the current and new data.
        suffixes = ("_old", "_new")
        merged_data = pd.merge(self.data, right, on=merge_on_cols, how="outer", suffixes=suffixes, sort=True)

        # Find all the data columns that are shared between the existing and new data
        shared_data_cols = set(self.data.columns) & set(right.columns) - set(merge_on_cols)

        merged_data = self._merge_shared_columns(
            merged_data=merged_data, shared_data_cols=shared_data_cols, suffixes=suffixes
        )

        return merged_data

    def _merge_shared_columns(self, merged_data: pd.DataFrame, shared_data_cols: List[str], suffixes: Tuple[str, str]):
        """
        Merge shared data columns in the updated dataframe.

        Some data columns are present in both the existing and new data. After the merge operation, these columns
        receive the suffixes to distinguish them. This method merges the old and new data and drops the suffixes.

        If the old and new data have different non-null values for any element of a subseries then the new value is
        used.

        Args:
            merged_data (pd.DataFrame): The new dataframe with the new data merged in.
            column (str): The name of the shared column to merge.
            suffixes (Tuple[str, str]): The suffixes used to distinguish the old and new data.

        """
        old_cols = [f"{col}{suffixes[0]}" for col in shared_data_cols]
        new_cols = [f"{col}{suffixes[1]}" for col in shared_data_cols]
        old_block = merged_data[old_cols]
        old_block.columns = shared_data_cols
        new_block = merged_data[new_cols]
        new_block.columns = shared_data_cols
        merged_block = new_block.combine_first(old_block)
        merged_data = pd.concat([merged_data.drop(old_cols + new_cols, axis=1), merged_block], axis=1)
        return merged_data

    def _validate_new_data(self, new_data: pd.DataFrame):
        """
        Validate the structure and index type of the new data.

        Args:
            new_data (pd.DataFrame): The new data to append. Should be a DataFrame with the same structure as the
            original data used to create the TimeFrame.

        Raises:
            KeyError: If the index or any of the identifier columns are missing in new_data.
            IndexTypeException: If the index type doesn't match.
        """
        if missing_cols := set(self.identifier_cols) - set(new_data.columns):
            raise KeyError(f"New data is missing identifier columns: {missing_cols}")

        if self.index_col not in set(new_data.columns):
            raise KeyError(f"New data should contain an '{self.index_col}' column.")

        if self.index_type == IndexTypeEnum.DATETIME and not pd.api.types.is_datetime64_dtype(new_data[self.index_col]):
            raise IndexTypeException("Index type of new data does not match the existing index type (datetime).")
        elif self.index_type == IndexTypeEnum.INTEGER and not pd.api.types.is_integer_dtype(new_data[self.index_col]):
            raise IndexTypeException("Index type of new data does not match the existing index type (integer).")

    # Accessing data
    # ------------------------------------------------------------------------------------------------------------------
    def get_time_index(
        self, series_id: IdentifierType, step_index: Union[int, Sequence[int]]
    ) -> Union[int, Sequence[int], pd.Timestamp, Sequence[pd.Timestamp]]:
        """
        Returns the time indexes at the desired steps of the series identified by 'identifier'.

        This function retrieves the first index and step size for the given identifier and
        calculates the index value at the nth step.

        Args:
            series_id (IdentifierType): Identifier for the subseries. It can be of type str or int.
            step_index (Union[int, Sequence[int]]): The step(s) at which to calculate the index value(s). Zero-based.

        Returns:
            Union[int, Sequence[int], pd.Timestamp, Sequence[pd.Timestamp]]: The index value(s) at the nth step(s).
            The type of the return value depends on the index_type of the TimeFrame (either int or pd.Timestamp) and
            the input type of 'index'.

        Raises:
            KeyError: If 'identifier' is not found in the TimeFrame.
            TypeError: If 'index' is not an integer or a sequence of integers.
        """
        # Retrieve the first index and step size for the given identifier
        first_index = self.zeroth_time_indexes[series_id]
        step_size = self.step_sizes[series_id]

        # Calculate the index value at the nth step
        if isinstance(step_index, int):
            return first_index + step_index * step_size
        return [first_index + i * step_size for i in step_index]

    def get_step_index(
        self, series_id: IdentifierType, time_index: Union[IndexType, Sequence[IndexType]]
    ) -> Union[int, List[int]]:
        """
        Given a series identifier and time index, returns the corresponding step index(es).

        Args:
            series_id (IdentifierType): Identifier for the subseries.
            time_index (Union[IndexType, Sequence[IndexType]]): The time index(es) to convert to step index(es).

        Returns:
            Union[int, List[int]]: The corresponding step index(es). The type of the return value depends
                on the input type of 'time_index'.

        Raises:
            KeyError: If 'identifier' is not found in the TimeFrame.
        """
        # Retrieve the DataFrame for the given identifier
        series_df = self.get_series_df(series_id=series_id)

        # Calculate the step index(es) for the given time index(es)
        if isinstance(time_index, collections.abc.Iterable):
            return [series_df.index.get_loc(index) for index in time_index]
        return series_df.index.get_loc(time_index)

    def get_series_df(self, series_id: IdentifierType) -> pd.DataFrame:
        """Get the series corresponding to a given identifier. Index columns are dropped and the time index is set.

        Args:
            series_id (IdentifierType): The identifier for the series to retrieve.

        Returns:
            pd.DataFrame: The series as a DataFrame.
        """
        if series_id not in self.groupby.groups:
            raise KeyError(f"Identifier not found: {series_id}")
        series = self.groupby.get_group(series_id).drop(columns=self.identifier_cols).set_index(self.index_col)

        # Set frequency
        if self.index_type == IndexTypeEnum.DATETIME:
            series.index = pd.DatetimeIndex(series.index, freq=self.step_sizes[series_id])
        elif self.index_type == IndexTypeEnum.INTEGER:
            # For integer index, ensure the step size
            series.index = pd.RangeIndex(
                start=series.index[0], stop=series.index[-1] + 1, step=self.step_sizes[series_id]
            )

        return series

    def get_series(self, series_ids: Optional[Union[IdentifierType, Iterable[IdentifierType]]] = None) -> TimeFrame:
        """Get the series corresponding to the supplied ids. Returns a copy of the series in a new TimeFrame.

        Args:
            series_ids (Union[IdentifierType, Iterable[IdentifierType]]): The identifiers of the series to retrieve.

        Returns:
            TimeFrame: The series as a new TimeFrame.
        """
        if series_ids is None:
            return self.copy()

        series_ids = self._parse_series_ids(series_ids)
        series = pd.concat([self.groupby.get_group(series_id) for series_id in series_ids])

        return TimeFrame(
            data=series,
            identifier_cols=self.identifier_cols,
            index_col=self.index_col,
            step_sizes=self.step_sizes,
        )

    def get_slice_by_time(
        self,
        series_ids: Optional[Union[IdentifierType, Iterable[IdentifierType]]] = None,
        start: Optional[IndexType] = None,
        stop: Optional[IndexType] = None,
    ) -> TimeFrame:
        """
        Returns a slice of a subseries (or multiple subseries) in the TimeFrame identified by the given identifier(s),
        between the start and stop values (inclusive) of the index column.

        Args:
            series_ids (Optional[Union[IdentifierType, List[IdentifierType]]]): Identifier(s) for the subseries. Each
                identifier can be a Tuple of str or int. If not provided, the operation will be applied to all subseries
                in the TimeFrame.
            start (Optional[IndexType]): The starting value of the index for the slice. If not provided, the slice
                starts from the beginning of each subseries.
            stop (Optional[IndexType]): The stopping value of the index for the slice (inclusive). If not provided,
                the slice ends at the end of each subseries.

        Returns:
            TimeFrame: A new TimeFrame containing the desired slice of the subseries.

        Raises:
            KeyError: If the provided identifier does not exist in the TimeFrame.
            TypeError: If the provided start or stop is not of the correct type.
        """

        # Validate the start and stop parameters
        if self.index_type == IndexTypeEnum.INTEGER:
            if start is not None and not isinstance(start, int):
                raise TypeError(f"start must be an integer or None, not {type(start)}.")
            if stop is not None and not isinstance(stop, int):
                raise TypeError(f"stop must be an integer or None, not {type(stop)}.")
        elif self.index_type == IndexTypeEnum.DATETIME:
            if start is not None and not isinstance(start, pd.Timestamp):
                raise TypeError(f"start must be a pandas Timestamp or None, not {type(start)}.")
            if stop is not None and not isinstance(stop, pd.Timestamp):
                raise TypeError(f"stop must be a pandas Timestamp or None, not {type(stop)}.")

        # Fetch the subseries
        selected_series = self.get_series(series_ids).data

        # Generate the boolean masks and perform slicing
        mask = (start is None or selected_series[self.index_col] >= start) & (
            stop is None or selected_series[self.index_col] <= stop
        )
        sliced_subseries = selected_series.loc[mask]

        return TimeFrame(
            data=sliced_subseries,
            index_col=self.index_col,
            identifier_cols=self.identifier_cols,
            step_sizes=self.step_sizes,
        )

    def get_slice_by_step(
        self,
        series_ids: Union[IdentifierType, Iterable[IdentifierType]],
        start: Optional[int] = None,
        stop: Optional[int] = None,
    ) -> TimeFrame:
        """
        Returns a slice of a series identified by 'identifier' from start to stop (inclusive),
        where start and stop are the step indices in the series.

        Args:
            series_ids (IdentifierType): Identifier for the series. It can be a Tuple of type str or int.
            start (int): The starting step index for the slice. If not provided, the slice will start at the beginning
            of the series.
            stop (int): The stopping step index for the slice (inclusive). If not provided, the slice will go till the
            end of the series.

        Returns:
            TimeFrame: A new TimeFrame containing the desired slice of the subseries.
        """

        series_ids = self._parse_series_ids(series_ids)
        sliced_series = pd.concat([self._get_slice_by_step_single(series_id, start, stop) for series_id in series_ids])

        return TimeFrame(
            data=sliced_series,
            index_col=self.index_col,
            identifier_cols=self.identifier_cols,
            step_sizes=self.step_sizes,
        )

    def _get_slice_by_step_single(
        self, identifier: IdentifierType, start: Optional[int] = None, stop: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Returns a slice of a single subseries identified by 'identifier' from start to stop (inclusive),
        where start and stop are the step indices in the subseries.

        Args:
            identifier (IdentifierType): Identifier for the subseries. It can be a Tuple of type str or int.
            start (int): The starting step index for the slice. If not provided, the slice will start at the beginning of the subseries.
            stop (int): The stopping step index for the slice (inclusive). If not provided, the slice will go till the end of the subseries.

        Returns:
            pd.DataFrame: A DataFrame containing the desired slice of the subseries.
        """
        subseries = self.groupby.get_group(identifier)

        if start is not None and not isinstance(start, int):
            raise TypeError(f"start must be an integer or None, not {type(start)}.")
        if stop is not None and not isinstance(stop, int):
            raise TypeError(f"stop must be an integer or None, not {type(stop)}.")

        if start is None:
            start = 0

        if stop is None:
            stop = len(subseries) - 1

        return subseries.iloc[start : stop + 1]

    def _parse_series_ids(
        self, series_ids: Optional[Union[IdentifierType, Iterable[IdentifierType]]] = None
    ) -> List[IdentifierType]:
        if series_ids is None:
            return list(self.groupby.groups.keys())
        if series_ids in self.groupby.groups:
            return [series_ids]
        elif missing_ids := [series_id for series_id in series_ids if series_id not in self.groupby.groups]:
            raise KeyError(f"Identifier(s) not found: {missing_ids}")
        return list(series_ids)

    def __getitem__(self, columns: List[str]) -> TimeFrame:
        """
        Returns a new TimeFrame with the specified columns, along with the 'index' and 'identifier' columns.

        Args:
            columns (List[str]): The columns to include in the returned TimeFrame.

        Returns:
            TimeFrame: A new TimeFrame with the specified columns.
        """
        if not isinstance(columns, list):
            raise TypeError(f"columns must be a list, not {type(columns)}.")

        if any(column in self.identifier_cols for column in columns):
            raise ValueError("TimeFrame.get_columns cannot be used to access identifier columns.")
        if self.index_col in columns:
            raise ValueError("TimeFrame.get_columns cannot be used to access the index column.")

        if any(column not in self.data.columns for column in columns):
            raise ValueError("One or more columns not found in the TimeFrame.")

        selected_columns = [self.index_col] + self.identifier_cols + columns
        return TimeFrame(
            data=self.data[selected_columns].copy(),
            index_col=self.index_col,
            identifier_cols=self.identifier_cols,
            step_sizes=self.step_sizes,
        )

    # Special methods
    # ------------------------------------------------------------------------------------------------------------------
    def __len__(self):
        """
        Returns the number of rows in the underlying data of the TimeFrame.

        :return: int, the number of rows in the underlying data
        """
        return len(self.data)

    def __eq__(self, other: object) -> bool:
        """Compares this TimeFrame to another object for equality.

        Args:
            other (object): The object to compare to this TimeFrame.

        Returns:
            bool: True if both are TimeFrame objects with equal attributes, False otherwise.
        """
        return (
            (
                self.data.equals(other.data)
                and self.index_type == other.index_type
                and self.step_sizes == other.step_sizes
                and self.index_col == other.index_col
                and self.identifier_cols == other.identifier_cols
                and self.zeroth_time_indexes == other.zeroth_time_indexes
            )
            if isinstance(other, TimeFrame)
            else False
        )

    # Properties
    # ------------------------------------------------------------------------------------------------------------------
    @property
    def last_observed_time_indexes(self) -> Mapping[IdentifierType, IndexType]:
        return {
            identifier: group.dropna().set_index(self.index_col).last_valid_index()
            for identifier, group in self.groupby
        }

    @property
    def index(self) -> pd.Series:
        return self.data[self.index_col]
