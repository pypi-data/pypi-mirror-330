import pandas as pd


from metaml._util.logger import AdvancedLogger


logger = AdvancedLogger(__name__).get_logger()


_escape_char_dict = str.maketrans(
    {
        "-": r"\-",
        "]": r"\]",
        "\\": r"\\",
        "^": r"\^",
        "$": r"\$",
        "*": r"\*",
        ".": r"\.",
    }
)


def get_escaped_string(string: str) -> str:
    """Returns a string in its escaped form"""
    return string.translate(_escape_char_dict)


def is_number(value: str) -> bool:
    """Check if a string can be converted to a number."""
    try:
        float(value)
        return True
    except ValueError:
        return False


def convert_nonnumeric_to_category_columns(X: pd.DataFrame) -> pd.DataFrame:
    """Convert object columns to category columns."""
    for column in X.select_dtypes(exclude="number").columns:
        X[column] = X[column].astype("category")
    return X
