from rekuest_next.structures.default import (
    get_default_structure_registry,
    id_shrink,
)
from rekuest_next.widgets import SearchWidget
from rekuest_next.api.schema import PortScope
from kraph.api.schema import *

structure_reg = get_default_structure_registry()

structure_reg.register_as_structure(
    Ontology,
    identifier="@kraph/ontology",
    aexpand=aget_ontology,
    ashrink=id_shrink,
    scope=PortScope.GLOBAL,
    default_widget=SearchWidget(
        query=SearchOntologiesQuery.Meta.document, ward="kraph"
    ),
)
structure_reg.register_as_structure(
    Graph,
    identifier="@kraph/graph",
    aexpand=aget_graph,
    ashrink=id_shrink,
    scope=PortScope.GLOBAL,
    default_widget=SearchWidget(query=SearchGraphsQuery.Meta.document, ward="kraph"),
)
structure_reg.register_as_structure(
    Reagent,
    identifier="@kraph/reagent",
    aexpand=aget_reagent,
    ashrink=id_shrink,
    scope=PortScope.GLOBAL,
    default_widget=SearchWidget(query=SearchReagentsQuery.Meta.document, ward="kraph"),
)

structure_reg.register_as_structure(
    StructureCategory,
    identifier="@kraph/structurecategory",
    aexpand=aget_structure_category,
    ashrink=id_shrink,
    scope=PortScope.GLOBAL,
    default_widget=SearchWidget(
        query=SearchStructureCategoryQuery.Meta.document, ward="kraph"
    ),
)

structure_reg.register_as_structure(
    GenericCategory,
    identifier="@kraph/genericcategory",
    aexpand=aget_generic_category,
    ashrink=id_shrink,
    scope=PortScope.GLOBAL,
    default_widget=SearchWidget(
        query=SearchGenericCategoryQuery.Meta.document, ward="kraph"
    ),
)


structure_reg.register_as_structure(
    MeasurementCategory,
    identifier="@kraph/measurementcategory",
    aexpand=aget_measurment_category,
    ashrink=id_shrink,
    scope=PortScope.GLOBAL,
    default_widget=SearchWidget(
        query=SearchMeasurmentCategoryQuery.Meta.document, ward="kraph"
    ),
)

structure_reg.register_as_structure(
    RelationCategory,
    identifier="@kraph/relationcategory",
    aexpand=aget_relation_category,
    ashrink=id_shrink,
    scope=PortScope.GLOBAL,
    default_widget=SearchWidget(
        query=SearchRelationCategoryQuery.Meta.document, ward="kraph"
    ),
)

structure_reg.register_as_structure(
    GraphQuery,
    identifier="@kraph/graphquery",
    aexpand=aget_graph_query,
    ashrink=id_shrink,
    scope=PortScope.GLOBAL,
    default_widget=SearchWidget(
        query=SearchGraphQueriesQuery.Meta.document, ward="kraph"
    ),
)

structure_reg.register_as_structure(
    ProtocolStep,
    identifier="@kraph/protocolstep",
    aexpand=aget_protocol_step,
    ashrink=id_shrink,
    scope=PortScope.GLOBAL,
    default_widget=SearchWidget(
        query=SearchProtocolStepsQuery.Meta.document, ward="kraph"
    ),
)

structure_reg.register_as_structure(
    GraphView,
    identifier="@kraph/graphview",
    aexpand=aget_graph_view,
    ashrink=id_shrink,
    scope=PortScope.GLOBAL,
    default_widget=SearchWidget(
        query=SearchGraphViewsQuery.Meta.document, ward="kraph"
    ),
)
