from metaml.parameter_space.graph import ParameterGraph

from .nodes import parameter_nodes
from .edges import constraint_edges


parameter_graph = ParameterGraph(parameters=parameter_nodes, constraints=constraint_edges)
