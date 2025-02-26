"""Defines the abstract interface for splitting data"""
from typing import Optional, Union, Any, Type
from abc import ABC, abstractmethod
import logging

from pydantic.v1 import BaseModel

from ..abstract_factory import new_factory
from ... import graphs

# ──────────────────────────────────────────────────────────────────────────── #


class HighchartsConverter(ABC):
    """Abstract interface to split a dataset into train and test"""

    LOGGER = logging.getLogger("preprocessor")

    def __init__(self):
        pass

    def convert(self, graph: graphs.Graph):
        converted_data = self.convert_data(graph.graphJson)
        description = self.convert_description(graph.description)
        graph_fields = graph.dict().get("graphFields")
        context = graph.dict().get("context")
        return graphs.HighchartsGraph(
            type="highcharts",
            data=converted_data,
            description=description,
            graphFields=graph_fields,
            context=context,
        )

    @staticmethod
    def convert_description(description: Optional[graphs.GraphDescription]):
        if description is None:
            return None
        return description.html

    @abstractmethod
    def convert_data(self, graph_data: graphs.GraphT) -> dict:
        """Converts the graph data given to Highcharts format"""


HighchartsConverterFactory = new_factory(graphs.GraphType, HighchartsConverter)


def convert_highcharts_graph(graph: Union[graphs.Graph, dict]) -> graphs.HighchartsGraph:
    if not isinstance(graph, graphs.Graph):
        graph = graphs.Graph[Any].parse_obj(graph)
    assert isinstance(graph, graphs.Graph)
    converter = HighchartsConverterFactory.create(graph.type)
    if converter is None:
        raise ValueError(
            f"No registered implementation for the graph type {graph.type}"
        )
    # Redefine graph model as the specific version
    graph_class: Type[BaseModel] = graphs.graph_to_class[graph.type]
    specific_graph = graphs.Graph[graph_class].parse_obj(graph.dict())
    converted_graph = converter.convert(specific_graph)
    return converted_graph


__all__ = ["HighchartsConverter", "HighchartsConverterFactory", "convert_highcharts_graph"]