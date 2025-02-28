from typing import Dict, Any, List
import math
from .vars import current_ontology, current_graph
from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from kraph.api.schema import MeasurementKind

def create_linked_expression(expression, graph=None):
    from kraph.api.schema import link_expression

    if graph is None:
        graph = current_graph.get()

    assert graph is not None, "Graph must be set"

    return link_expression(expression=expression, graph=graph)


def s(name, description=None):
    from kraph.api.schema import create_structure_category

    exp = create_structure_category(
        label=name,
        ontology=current_ontology.get(),
        description=description,
    )
    return exp


def e(name, description=None):
    from kraph.api.schema import create_generic_category

    exp = create_generic_category(
        label=name,
        ontology=current_ontology.get(),
        description=description,
    )
    return exp


def r(name, description=None):
    from kraph.api.schema import create_relation_category

    exp = create_relation_category(
        label=name,
        ontology=current_ontology.get(),
        description=description,
    )
    return exp


def m(name, metric_kind: "MeasurementKind", description=None):
    from kraph.api.schema import create_measurement_category

    exp = create_measurement_category(
        label=name,
        kind=metric_kind,
        ontology=current_ontology.get(),
        description=description,
    )
    return exp
