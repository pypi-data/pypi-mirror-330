"""Parameter graph representation. Represents a parameter graph specifying the
domains of parameters and constraints between them.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import (
    List,
    Any,
    Optional,
    Union,
    Dict,
    Sequence,
    Iterator,
    Set,
    Tuple,
    Type,
)
from optuna import Trial, Study
from pydantic import BaseModel
import networkx as nx
import random


from metaml.parameter_space.node import (
    CategoricalNode,
    FloatNode,
    IntegerNode,
    MixedNode,
    DomainSet,
    FloatDistribution,
    IntegerDistribution,
)
from metaml.parameter_space.map import Mapping, ConstraintEdge
from metaml.parameter_space.set import FloatSet, CategoricalSet, IntegerSet, MixedSet
from metaml.factory.parameter_settings import (
    InputParameter,
    ParameterType,
    ParamSettings,
)
from metaml.exceptions import OptunaCategoricalConstraintViolation


ParameterNodeType = Union[CategoricalNode, FloatNode, IntegerNode, MixedNode]
"""A type alias for a parameter node."""


@dataclass
class NodeData:
    """
    A dataclass for representing a node in a parameter graph.

    Attributes:
        parameter (ParameterNodeType): The parameter associated with the node.
        dynamic_domain (Optional[DomainSet]): The dynamic domain of the node.
            This domain may change during operations like sampling or validation.
    """

    parameter: ParameterNodeType
    dynamic_domain: Optional[DomainSet] = None


@dataclass
class EdgeData:
    """
    A dataclass for representing an edge in a parameter graph.

    Attributes:
        mapping (Mapping): The constraint associated with the edge.
        incompatible_source_domain (Optional[DomainSet]): The domain of values for the source node
            that are incompatible with the constraint.
        incompatible_target_domain (Optional[DomainSet]): The domain of values for the target node
            that are incompatible with the constraint.
    """

    mapping: Mapping
    incompatible_source_domain: Optional[DomainSet] = None
    incompatible_target_domain: Optional[DomainSet] = None


class ParameterGraphModel(BaseModel):
    parameters: List[ParameterNodeType]
    constraints: List[ConstraintEdge]

    input_parameters: List[InputParameter]  # Deprecated


class ParameterGraph:
    """
    A class that represents a parameter graph specifying the domains of parameters and constraints between them.
    Parameters are represented by nodes in the graph and constraints are represented by edges.

    Attributes:
        graph (nx.DiGraph): A directed graph object from the networkx library that stores the parameter graph.
    """

    graph: nx.DiGraph

    def __init__(
        self,
        parameters: Optional[Sequence[ParameterNodeType]] = None,
        constraints: Optional[Sequence[ConstraintEdge]] = None,
        validate: bool = True,
    ) -> None:
        """Creates a parameter graph from a list of parameters and constraints."""

        self.graph = nx.DiGraph()

        for p in parameters or []:
            self.add_node(p)

        for c in constraints or []:
            self.add_edge(
                source=c[0],
                target=c[1],
                mapping=c[2],
            )

        if validate:
            if not self.validate_arc_consistency(reinitialize_domains=True):
                incompatible_domains = self.get_incompatible_domains()
                raise ValueError(
                    f"Parameter graph is not arc consistent. Incompatible domains:\n{incompatible_domains}"
                )
            self.teardown_dynamic_domains()

            # Convert the graph to an undirected graph
            undirected_graph = self.graph.to_undirected()

            # Check if the graph is acyclic
            if len(nx.cycle_basis(undirected_graph)) != 0:
                raise ValueError("Parameter graph is not acyclic so we cannot guarantee consistency of the parameters.")

    # -------------------------------------------------------------------------------------------- #
    # Construction Methods
    def add_node(self, node: ParameterNodeType) -> None:
        """Add a parameter to the parameter graph."""
        if node.name in self.graph.nodes:
            raise ValueError(f"Node with name '{node.name}' already exists.")

        # Create an instance of NodeData
        node_data = NodeData(parameter=node)
        self.graph.add_node(node.name, data=node_data)

    def _check_node_exists(self, node_name: str) -> None:
        if node_name not in self.graph.nodes:
            raise ValueError(f"Node with name '{node_name}' does not exist.")

    def _check_domain_type(self, node_name: str, mapping_type: Type[DomainSet]) -> None:
        node_domain_type = type(self.get_node_data(node_name).parameter.domain)
        if node_domain_type != mapping_type:
            raise TypeError(
                f"The domain type for node '{node_name}' must match the mapping's domain type. Got '{node_domain_type}' instead of '{mapping_type}'."
            )

    def _check_mapping_coverage(self, node_name: str, mapping_sets: List[DomainSet]) -> None:
        node = self.get_node_data(node_name).parameter
        coverage = type(node.domain)()
        for mapping_set in mapping_sets:
            coverage = coverage.union(mapping_set)

        if domain_difference := node.domain.difference(coverage):
            raise ValueError(
                f"The constraint map keys for node '{node_name}' do not cover the domain. Uncovered domain: {domain_difference}."
            )

    def add_edge(self, source: str, target: str, mapping: Mapping) -> None:
        """Add a constraint to the parameter graph.

        Args:
            source (str): The name of the source node.
            target (str): The name of the target node.
            mapping (Mapping): The constraint mapping between the source and target nodes.

        """

        self._check_node_exists(source)
        self._check_domain_type(source, mapping.source_type)

        self._check_node_exists(target)
        self._check_domain_type(target, mapping.target_type)

        if not isinstance(mapping, Mapping):
            raise ValueError("Constraint must be of type Mapping.")

        self._check_mapping_coverage(source, [item.source for item in mapping.items])
        self._check_mapping_coverage(target, [item.target for item in mapping.items])

        if self.graph.has_edge(source, target):
            raise ValueError(f"Edge between '{source}' and '{target}' already exists.")

        edge_data = EdgeData(mapping=mapping)
        self.graph.add_edge(source, target, data=edge_data)

    # -------------------------------------------------------------------------------------------- #
    # Getters adding type hints
    def nodes(self) -> Iterator[Tuple[str, NodeData]]:
        """Iterator over the nodes of this graph providing typing."""
        for node_name, node_data in self.graph.nodes(data=True):
            if node_data is not None:
                yield node_name, node_data["data"]

    def get_node_data(self, name: str) -> NodeData:
        """Returns the node with the given name providing typing."""
        return self.graph.nodes[name]["data"]

    def edges(self) -> Iterator[Tuple[str, str, EdgeData]]:
        """Iterator over the edges of this graph providing typing."""
        for edge_tuple in self.graph.edges(data=True):
            assert len(edge_tuple) == 3  # data=True ensures this
            source, target, edge_data = edge_tuple
            if edge_data is not None:
                yield source, target, edge_data["data"]

    def get_edge_data(self, source: str, target: str) -> EdgeData:
        """Returns the node with the given name providing typing."""
        return self.graph.edges[source, target]["data"]

    # -------------------------------------------------------------------------------------------- #
    # Validation Methods
    def setup_dynamic_domains(self):
        """
        Setup the dynamic domains for validation and sampling.

        Each parameter node has a static domain to define the parameter space we would like to explore.
        Dynamic domains, on the other hand, are mutable and allow us to keep track of all valid options
        of parameters during sampling.

        For each node in the parameter graph, this function accomplishes the following tasks:
            1. If the node is enabled, a copy of the node's static domain is assigned to the dynamic domain.
            2. If the node is disabled, a singleton domain containing the node's default value is created
               using the singleton method, and this singleton domain is assigned as the dynamic domain.
        """
        for node_name, node_data in self.nodes():
            node_data.dynamic_domain = (
                node_data.parameter.domain.copy()
                if node_data.parameter.enabled
                else node_data.parameter.domain.unit(node_data.parameter.default_value)
            )
        for source_name, target_name, edge_data in self.edges():
            edge_data.incompatible_source_domain = None
            edge_data.incompatible_target_domain = None

    def teardown_dynamic_domains(self):
        """Remove the dynamic domains to tidy up after sampling or validation."""
        for node_name, node_data in self.nodes():
            node_data.dynamic_domain = None
        for source_name, target_name, edge_data in self.edges():
            edge_data.incompatible_source_domain = None
            edge_data.incompatible_target_domain = None

    def validate_arc_consistency(self, reinitialize_domains=False) -> bool:
        """
        Checks if the graph is arc consistent. Inconsistent domains are stored in the edge data. Arc consistency in a
        constraint graph is achieved when for every node, each value in its domain can be paired with a valid value in
        the domain of every connected node based on the defined constraints.

        Args:
            reinitialize_domains (bool): If true, the domains will be reinitialized before the check. By default the
            domains will be reused since this method will be used repeatedly to apply constraints after each parameter
            is sampled.

        Returns:
            bool: Returns True if the graph is arc consistent, False otherwise.
        """
        if reinitialize_domains:
            self.setup_dynamic_domains()

        all_compatible = True

        # Iterate over all edges in the graph using the edges getter
        for source, target, edge_data in self.edges():
            # Get the constraint of the current edge from edge_data
            mapping = edge_data.mapping

            # Get the domains of the nodes on the current edge
            source_domain = self.get_node_data(source).dynamic_domain
            target_domain = self.get_node_data(target).dynamic_domain

            # self.setup_dynamic_domains() should ensure this property
            assert source_domain is not None
            assert target_domain is not None

            # Find incompatible values in the domains
            incompatible_source_domain = source_domain.difference(mapping.backward(target_domain))
            incompatible_target_domain = target_domain.difference(mapping.forward(source_domain))

            # Store the incompatible domains in the edge data
            self.get_edge_data(source, target).incompatible_source_domain = incompatible_source_domain
            self.get_edge_data(source, target).incompatible_target_domain = incompatible_target_domain

            # If incompatible domains are not empty, then the graph is not arc consistent
            if not (incompatible_source_domain.is_empty and incompatible_target_domain.is_empty):
                all_compatible = False

        return all_compatible

    def get_incompatible_domains(self) -> str:
        """
        Returns a string representation of all incompatible domains in the graph.

        Returns:
            str: String representation of all incompatible domains in the graph.
        """
        incompatible_domains = [
            f"Edge {(source, target)}:\n"
            f"Incompatible sources: {repr(data.incompatible_source_domain)}\n"
            f"Incompatible targets: {repr(data.incompatible_target_domain)}"
            for source, target, data in self.edges()
        ]
        return "\n".join(incompatible_domains)

    # -------------------------------------------------------------------------------------------- #
    # Sampling Methods
    def update_sample_domains(self) -> bool:
        """
        Update the sample domains based on the results of validate_arc_consistency.

        Returns:
            bool: Returns True if the graph is arc consistent, otherwise domains are updated and False is returned.
        """

        if self.validate_arc_consistency(reinitialize_domains=False):
            return True

        # Iterate over all edges in the graph
        for source, target, edge_data in self.edges():
            incompatible_source_domain = edge_data.incompatible_source_domain
            incompatible_target_domain = edge_data.incompatible_target_domain

            if incompatible_target_domain is None or incompatible_source_domain is None:
                raise ValueError(
                    f"Incompatible domains not found. They should be set by validate_arc_consistency: {incompatible_source_domain}, {incompatible_target_domain}."
                )

            # Get the current sample domains of the nodes
            source_domain = self.get_node_data(source).dynamic_domain
            target_domain = self.get_node_data(target).dynamic_domain

            if source_domain is None or target_domain is None:
                raise ValueError(
                    f"Sample domains not found. They should be set by setup_dynamic_domains: {source_domain}, {target_domain}."
                )

            # Remove the incompatible values from the sample domains
            self.get_node_data(source).dynamic_domain = source_domain.difference(incompatible_source_domain)
            self.get_node_data(target).dynamic_domain = target_domain.difference(incompatible_target_domain)

            # Reset the incompatible domains
            edge_data.incompatible_source_domain = None
            edge_data.incompatible_target_domain = None

        return False

    def apply_arc_consistency(self):
        """
        Prunes the parameter domains of the graph until arc consistency is achieved. Arc consistency in a constraint
        graph is achieved when for every node, each value in its domain can be paired with a valid value in the domain
        of every connected node based on the defined constraints.

        This method repeatedly updates the sample domains until the graph becomes arc consistent.
        """
        while not self.update_sample_domains():
            ...

    def sample_node(self, node) -> Union[FloatSet, IntegerSet, CategoricalSet, MixedSet]:
        """
        Sample from the dynamic domain of a given node in the graph.

        This method retrieves the node's data and utilizes its specific sampling method to generate sample from the
        desired distribution.

        Args:
            node: The node (identified by its name) to sample from in the graph.

        Returns:
            A sampled value from the node's dynamic domain, which could be of types FloatSet, IntegerSet,
            CategoricalSet, or MixedSet.
        """
        # Retrieve the node object
        parameter_node = self.get_node_data(node).parameter

        # Retrieve sample domain
        sample_domain = self.get_node_data(node).dynamic_domain

        # Use the node's sample method to sample from the domain
        return parameter_node.sample(sample_domain)

    def sample(self) -> Dict[str, Any]:
        """
        Iterate over all nodes in the graph and sample from their dynamic domains.

        During the sampling process, the method also applies arc consistency to enforce constraints. After each node is
        sampled, its dynamic domain is replaced with a singleton containing the sampled value.

        Returns:
            A dictionary with the node names as keys and their corresponding sampled values as values.
        """

        sampled_values = {}

        self.setup_dynamic_domains()

        # Randomise and iterate over all nodes in the graph
        randomized_nodes = list(self.nodes())
        random.shuffle(randomized_nodes)
        for node_name, node_data in randomized_nodes:
            self.apply_arc_consistency()

            # Sample a value from the node's domain
            sampled_singleton = self.sample_node(node_name)
            sampled_values[node_name] = sampled_singleton.value

            # Replace the sample domain with a singleton containing the sampled value
            self.get_node_data(node_name).dynamic_domain = sampled_singleton

        return sampled_values

    # -------------------------------------------------------------------------------------------- #
    # IO Methods
    @classmethod
    def from_param_settings(cls, param_settings: ParamSettings) -> ParameterGraph:
        """Class constructor to build a ParameterGraph from a ParamSettings object."""
        parameter_nodes = param_settings.to_nodes()
        return cls(parameters=parameter_nodes)

    def to_input_parameters(self) -> List[InputParameter]:
        """Converts the nodes of the parameter graph to the InputParameter pydantic model representation."""

        input_parameters = []

        for node_name, node_data in self.nodes():
            domain: Union[CategoricalSet, FloatSet, IntegerSet, MixedSet] = node_data.parameter.domain

            values: Set[Any] = set()

            if isinstance(domain, IntegerSet):
                parameter_type = ParameterType.INT
                min_value, max_value = domain.lower_bound, domain.upper_bound - 1
            elif isinstance(domain, FloatSet):
                parameter_type = ParameterType.FLOAT
                min_value, max_value = domain.lower_bound, domain.upper_bound
            elif isinstance(domain, CategoricalSet):
                min_value, max_value = None, None
                if domain.categories.difference({True, False}) == set():
                    parameter_type = ParameterType.BOOLEAN
                else:
                    parameter_type = ParameterType.LIST
                    values = domain.categories
            elif isinstance(domain, MixedSet):
                parameter_type = ParameterType.LIST
                if domain.integer_set:
                    min_value, max_value = (
                        domain.integer_set.lower_bound,
                        domain.integer_set.upper_bound - 1,
                    )
                elif domain.float_set:
                    min_value, max_value = (
                        domain.float_set.lower_bound,
                        domain.float_set.upper_bound,
                    )
                else:
                    min_value, max_value = None, None
                values = domain.categorical_set.categories
            else:
                raise ValueError("Unsupported domain type")

            input_param = InputParameter(
                parameterName=node_data.parameter.name,
                parameterType=parameter_type,
                minValue=min_value,
                maxValue=max_value,
                values=values,
                defaultValue=node_data.parameter.default_value,
                label=node_data.parameter.label,
                description=node_data.parameter.description,
                enabled=node_data.parameter.enabled,
                constraint=node_data.parameter.constraint,
                constraintInformation=node_data.parameter.constraintInformation,
            )
            input_parameters.append(input_param)

        return input_parameters

    def export(self) -> ParameterGraphModel:
        input_parameters = self.to_input_parameters()
        parameters = [node_data.parameter for _, node_data in self.nodes()]
        constraints = [
            ConstraintEdge(source=source, target=target, mapping=edge_data.mapping)
            for source, target, edge_data in self.edges()
        ]
        return ParameterGraphModel(
            parameters=parameters,
            constraints=constraints,
            input_parameters=input_parameters,
        )

    # -------------------------------------------------------------------------------------------- #
    # Special Methods
    def __eq__(self, other: Union[ParameterGraph, Any]) -> bool:
        """Tests if two parameter graphs are equal."""
        if isinstance(other, ParameterGraph):
            return nx.is_isomorphic(
                self.graph,
                other.graph,
                node_match=lambda n1, n2: n1 == n2,
                edge_match=lambda e1, e2: e1 == e2,
            )
        return False

    # -------------------------------------------------------------------------------------------- #
    # Optuna Methods
    def optuna_sample_categorical(self, trial: Trial, node_name: str) -> Any:
        """
        Suggest a value for a CategoricalNode using an Optuna trial. A safe categorical suggestion method is used which
        to handle the fact that Optuna that doesn't allow dynamic control over the domain of categorical parameters.

        Args:
            trial (Trial): The Optuna trial to use for sampling.
            node_name (str): The name of the node from which to sample.

        Returns:
            Any: The suggested value for the categorical node.
        """
        allowed_domain = self.get_node_data(node_name).dynamic_domain
        return self.suggest_categorical_safe(trial, node_name, allowed_domain)

    def suggest_categorical_safe(self, trial: Trial, node_name: str, allowed_domain: CategoricalSet) -> Any:
        """
        Suggest a value from a categorical domain in a safe manner. This function uses Optuna's
        suggest_categorical method but adds an additional check to ensure the suggested value
        is within the allowed domain. It is designed to handle the constraint of Optuna that
        doesn't allow dynamic control over the domain of categorical parameters.

        If the suggested value is not within the allowed domain, it raises an
        OptunaCategoricalConstraintViolation.

        Args:
            trial (Trial): The Optuna trial to use for suggesting the value.
            node_name (str): The name of the node for which a value is to be suggested.
            allowed_domain (CategoricalSet): The allowed domain of values for this node.

        Returns:
            Any: The suggested value that is within the allowed domain.

        Raises:
            OptunaCategoricalConstraintViolation: If the suggested value is not in the allowed domain.
        """
        maximum_categorical_domain = sorted(
            list(self.get_node_data(node_name).parameter.maximum_categorical_domain.categories)
        )
        value = trial.suggest_categorical(node_name, maximum_categorical_domain)
        if value in allowed_domain.categories:
            return value
        raise OptunaCategoricalConstraintViolation(
            f"Value {value} is not in allowed domain {allowed_domain.categories}"
        )

    def optuna_sample_integer(self, trial: Trial, node_name: str) -> int:
        """
        Sample an integer parameter from a given node using an Optuna trial. The domain from which the value is sampled
        should be an integer interval.

        Args:
            trial (Trial): The Optuna trial to use for sampling.
            node_name (str): The name of the node from which to sample.

        Returns:
            int: The sampled integer value.

        Raises:
            ValueError: If the domain isn't an integer interval.
        """
        node_data = self.get_node_data(node_name)
        sample_domain = node_data.dynamic_domain
        if not isinstance(sample_domain, IntegerSet) or not sample_domain.is_interval:
            raise ValueError(f"Cannot sample from non-interval domain {sample_domain}.")

        log = node_data.parameter.distribution == IntegerDistribution.LOG_UNIFORM
        return trial.suggest_int(
            node_name,
            sample_domain.lower_bound,
            sample_domain.upper_bound - 1,  # Trial.suggest_int is inclusive on both ends
            log=log,
        )

    def optuna_sample_float(self, trial: Trial, node_name: str) -> float:
        """
        Sample a float parameter from a given node using an Optuna trial. The domain from which the value is sampled
        should be a float interval.

        Args:
            trial (Trial): The Optuna trial to use for sampling.
            node_name (str): The name of the node from which to sample.

        Returns:
            float: The sampled float value.

        Raises:
            ValueError: If the domain isn't a float interval.
        """
        node_data = self.get_node_data(node_name)
        sample_domain = node_data.dynamic_domain
        if not isinstance(sample_domain, FloatSet) or not sample_domain.is_interval:
            raise ValueError(f"Cannot sample from non-interval domain {sample_domain}.")

        log = node_data.parameter.distribution == FloatDistribution.LOG_UNIFORM
        return trial.suggest_float(
            node_name,
            sample_domain.lower_bound,
            sample_domain.upper_bound,
            log=log,
        )

    def optuna_sample_mixed(self, trial: Trial, node_name: str) -> Union[str, bool, int, float, None]:
        """
        Sample a mixed parameter from a given node using an Optuna trial.

        Optuna does not allow for parameters to be a mixture of integer, float, and categorical values so we first
        randomly choose the subtype of the mixed parameter to sample from. Each MixedNode has a primary type and if the
        chosen subtype is the primary type, we sample use the Optuna trial object to sample from the domain. Otherwise
        we sample the parameter independently and it won't be registered with Optuna.

        Args:
            trial (Trial): The Optuna trial to use for sampling.
            node_name (str): The name of the node from which to sample.

        Returns:
            Union[str, bool, int, float, None]: The sampled value.

        Raises:
            TypeError: If the subset type is unsupported.
        """
        node_data = self.get_node_data(node_name)
        sample_domain = node_data.dynamic_domain
        subset = node_data.parameter.choose_subset(sample_domain)

        if type(subset) != node_data.parameter.primary_type:
            return node_data.parameter.sample(subset).value
        if isinstance(subset, FloatSet):
            return trial.suggest_float(
                node_name,
                subset.lower_bound,
                subset.upper_bound,
                log=node_data.parameter.float_distribution == FloatDistribution.LOG_UNIFORM,
            )
        elif isinstance(subset, IntegerSet):
            return trial.suggest_int(
                node_name,
                subset.lower_bound,
                subset.upper_bound,
                log=node_data.parameter.integer_distribution == IntegerDistribution.LOG_UNIFORM,
            )
        elif isinstance(subset, CategoricalSet):
            return self.suggest_categorical_safe(trial, node_name, subset)
        else:
            raise TypeError(f"Unsupported subset type {type(subset)}.")

    def optuna_sample(self, trial: Trial) -> Dict[str, Any]:
        """
        Sample from the parameter graph using an Optuna trial.

        This method uses an Optuna trial to sample parameters from the graph. The method applies arc consistency after
        each sample is taken in order to enforce constraints. At the end it returns a dictionary of sampled parameters.

        Args:
            trial (Trial): The Optuna trial to use for sampling.

        Returns:
            Dict[str, Any]: A dictionary of sampled parameters. Each key-value pair represents
            a parameter name and its sampled value.

        Raises:
            OptunaCategoricalConstraintViolation: If a suggested categorical value is not within the allowed domain.
            This is because Optuna does not support dynamic control over the domain of categorical parameters.
        """

        if not nx.is_directed_acyclic_graph(self.graph):
            raise ValueError("The parameter graph contains a cycle, and thus cannot be sorted topologically.")

        sampled_parameters: Dict[str, Any] = {}

        self.setup_dynamic_domains()
        self.apply_arc_consistency()

        # Randomise and iterate over all nodes in the graph
        randomized_nodes = list(self.nodes())
        random.shuffle(randomized_nodes)
        for node_name, node_data in randomized_nodes:
            sample_domain = node_data.dynamic_domain
            if sample_domain is None:
                raise ValueError(
                    f"Node {node_name} has no dynamic domain. This should be set by setup_dynamic_domains."
                )

            value: Any = None
            if isinstance(node_data.parameter, FloatNode):
                value = self.optuna_sample_float(trial=trial, node_name=node_name)

            elif isinstance(node_data.parameter, CategoricalNode):
                value = self.optuna_sample_categorical(trial=trial, node_name=node_name)

            elif isinstance(node_data.parameter, IntegerNode):
                value = self.optuna_sample_integer(trial=trial, node_name=node_name)

            elif isinstance(node_data.parameter, MixedNode):
                value = self.optuna_sample_mixed(trial=trial, node_name=node_name)

            else:
                raise ValueError(f"Unsupported node type {type(node_data.parameter)}.")

            sampled_parameters[node_name] = value
            # Update the sample_domain with the sampled value
            node_data.dynamic_domain = sample_domain.unit(value)
            # Apply arc consistency after each iteration
            self.apply_arc_consistency()

        self.teardown_dynamic_domains()

        return sampled_parameters

    def generate_trial(self, study: Study, max_attempts: int = 1000) -> Tuple[Dict[str, Any], Trial]:
        """
        Generate a trial from a study and sample parameters using the trial. Keep generating trials until a successful
        one is produced. Optuna doesn't allow us to dynamically control the domain of categorical parameters, we sample
        categorical parameters repeatedly until we find a configuration which obeys the constraints.

        Args:
            study (Study): The Optuna study to use for generating the trial.
            max_attempts (int, optional): Maximum number of trial generation attempts.
                Defaults to 1000.

        Returns:
            Tuple[Dict[str, Any], Trial]: A tuple of the sampled parameters dictionary and the trial.

        Raises:
            RuntimeError: If a valid trial is not found after max_attempts.
        """
        attempts = 0
        while attempts < max_attempts:
            try:
                trial = study.ask()
                sampled_parameters = self.optuna_sample(trial)
                return sampled_parameters, trial
            except OptunaCategoricalConstraintViolation:
                attempts += 1
                continue
        raise RuntimeError(f"Unable to generate a valid trial after {max_attempts} attempts.")

    # -------------------------------------------------------------------------------------------- #
    # Other methods
    def enable_all(self):
        """Enables all parameters in the graph."""
        for node_name, node_data in self.nodes():
            node_data.parameter.enabled = True
