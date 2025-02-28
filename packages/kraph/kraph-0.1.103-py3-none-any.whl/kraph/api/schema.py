from typing import Union, Literal, List, Any, Optional, Annotated, Tuple, Iterable
from kraph.funcs import execute, aexecute
from enum import Enum
from pydantic import Field, BaseModel, ConfigDict
from kraph.traits import (
    OntologyTrait,
    StructureCategoryTrait,
    EntityTrait,
    RelationCategoryTrait,
    StructureTrait,
    GraphTrait,
    GenericCategoryTrait,
    MeasurementCategoryTrait,
    HasPresignedDownloadAccessor,
)
from kraph.rath import KraphRath
from kraph.scalars import (
    StructureIdentifier,
    RemoteUpload,
    Cypher,
    StructureString,
    NodeID,
)
from rath.scalars import ID
from datetime import datetime


class ViewKind(str, Enum):
    PATH = "PATH"
    PAIRS = "PAIRS"
    TABLE = "TABLE"
    INT_METRIC = "INT_METRIC"
    FLOAT_METRIC = "FLOAT_METRIC"


class ColumnKind(str, Enum):
    NODE = "NODE"
    VALUE = "VALUE"
    EDGE = "EDGE"


class MeasurementKind(str, Enum):
    INT = "INT"
    FLOAT = "FLOAT"
    DATETIME = "DATETIME"
    STRING = "STRING"
    CATEGORY = "CATEGORY"
    BOOLEAN = "BOOLEAN"
    THREE_D_VECTOR = "THREE_D_VECTOR"
    TWO_D_VECTOR = "TWO_D_VECTOR"
    ONE_D_VECTOR = "ONE_D_VECTOR"
    FOUR_D_VECTOR = "FOUR_D_VECTOR"
    N_VECTOR = "N_VECTOR"


class InstanceKind(str, Enum):
    LOT = "LOT"
    SAMPLE = "SAMPLE"
    ENTITY = "ENTITY"
    UNKNOWN = "UNKNOWN"


class GraphInput(BaseModel):
    name: str
    ontology: Optional[ID] = None
    experiment: Optional[ID] = None
    description: Optional[str] = None
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class GraphViewInput(BaseModel):
    """Input for creating a new expression"""

    query: ID
    graph: ID
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class NodeViewInput(BaseModel):
    """Input for creating a new expression"""

    query: ID
    node: ID
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class ScatterPlotInput(BaseModel):
    """Input for creating a new expression"""

    query: ID
    "The query to use"
    name: str
    "The label/name of the expression"
    description: Optional[str] = None
    "A detailed description of the expression"
    id_column: str = Field(alias="idColumn")
    "The column to use for the ID of the points"
    x_column: str = Field(alias="xColumn")
    "The column to use for the x-axis"
    x_id_column: Optional[str] = Field(alias="xIdColumn", default=None)
    "The column to use for the x-axis ID (node, or edge)"
    y_column: str = Field(alias="yColumn")
    "The column to use for the y-axis"
    y_id_column: Optional[str] = Field(alias="yIdColumn", default=None)
    "The column to use for the y-axis ID (node, or edge)"
    size_column: Optional[str] = Field(alias="sizeColumn", default=None)
    "The column to use for the size of the points"
    color_column: Optional[str] = Field(alias="colorColumn", default=None)
    "The column to use for the color of the points"
    shape_column: Optional[str] = Field(alias="shapeColumn", default=None)
    "The column to use for the shape of the points"
    test_against: Optional[ID] = Field(alias="testAgainst", default=None)
    "The graph to test against"
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class PlotViewInput(BaseModel):
    """Input for creating a new expression"""

    plot: ID
    view: ID
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class RelationInput(BaseModel):
    """Input type for creating a relation between two entities"""

    left: ID
    "ID of the left entity (format: graph:id)"
    right: ID
    "ID of the right entity (format: graph:id)"
    kind: ID
    "ID of the relation kind (LinkedExpression)"
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class MeasurementInput(BaseModel):
    structure: NodeID
    entity: NodeID
    expression: ID
    value: Optional[Any] = None
    valid_from: Optional[datetime] = Field(alias="validFrom", default=None)
    valid_to: Optional[datetime] = Field(alias="validTo", default=None)
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class StructureInput(BaseModel):
    structure: StructureString
    graph: Optional[ID] = None
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class ReagentInput(BaseModel):
    lot_id: str = Field(alias="lotId")
    expression: ID
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class ProtocolStepInput(BaseModel):
    """Input type for creating a new protocol step"""

    template: ID
    "ID of the protocol step template"
    entity: ID
    "ID of the entity this step is performed on"
    reagent_mappings: Tuple["ReagentMappingInput", ...] = Field(alias="reagentMappings")
    "List of reagent mappings"
    value_mappings: Tuple["VariableInput", ...] = Field(alias="valueMappings")
    "List of variable mappings"
    performed_at: Optional[datetime] = Field(alias="performedAt", default=None)
    "When the step was performed"
    performed_by: Optional[ID] = Field(alias="performedBy", default=None)
    "ID of the user who performed the step"
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class ReagentMappingInput(BaseModel):
    """Input type for mapping reagents to protocol steps"""

    reagent: ID
    "ID of the reagent to map"
    volume: int
    "Volume of the reagent in microliters"
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class VariableInput(BaseModel):
    """Input type for mapping variables to protocol steps"""

    key: str
    "Key of the variable"
    value: str
    "Value of the variable"
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class CreateModelInput(BaseModel):
    """Input type for creating a new model"""

    name: str
    "The name of the model"
    model: RemoteUpload
    "The uploaded model file (e.g. .h5, .onnx, .pt)"
    view: Optional[ID] = None
    "Optional view ID to associate with the model"
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class RequestMediaUploadInput(BaseModel):
    key: str
    datalayer: str
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class EntityInput(BaseModel):
    """Input type for creating a new entity"""

    graph: ID
    expression: ID
    "The ID of the kind (LinkedExpression) to create the entity from"
    name: Optional[str] = None
    "Optional name for the entity"
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class OntologyInput(BaseModel):
    """Input type for creating a new ontology"""

    name: str
    "The name of the ontology (will be converted to snake_case)"
    description: Optional[str] = None
    "An optional description of the ontology"
    purl: Optional[str] = None
    "An optional PURL (Persistent URL) for the ontology"
    image: Optional[ID] = None
    "An optional ID reference to an associated image"
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class GraphQueryInput(BaseModel):
    """Input for creating a new expression"""

    ontology: Optional[ID] = None
    "The ID of the ontology this expression belongs to. If not provided, uses default ontology"
    name: str
    "The label/name of the expression"
    query: Cypher
    "The label/name of the expression"
    description: Optional[str] = None
    "A detailed description of the expression"
    kind: ViewKind
    "The kind/type of this expression"
    columns: Optional[Tuple["ColumnInput", ...]] = None
    "The columns (if ViewKind is Table)"
    test_against: Optional[ID] = Field(alias="testAgainst", default=None)
    "The graph to test against"
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class ColumnInput(BaseModel):
    name: str
    kind: ColumnKind
    label: Optional[str] = None
    description: Optional[str] = None
    expression: Optional[ID] = None
    value_kind: Optional[MeasurementKind] = Field(alias="valueKind", default=None)
    searchable: Optional[bool] = None
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class NodeQueryInput(BaseModel):
    """Input for creating a new expression"""

    ontology: Optional[ID] = None
    "The ID of the ontology this expression belongs to. If not provided, uses default ontology"
    name: str
    "The label/name of the expression"
    query: Cypher
    "The label/name of the expression"
    description: Optional[str] = None
    "A detailed description of the expression"
    kind: ViewKind
    "The kind/type of this expression"
    columns: Optional[Tuple[ColumnInput, ...]] = None
    "The columns (if ViewKind is Table)"
    test_against: Optional[ID] = Field(alias="testAgainst", default=None)
    "The node to test against"
    allowed_entities: Optional[Tuple[ID, ...]] = Field(
        alias="allowedEntities", default=None
    )
    "The allowed entitie classes for this query"
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class MeasurementCategoryInput(BaseModel):
    """Input for creating a new expression"""

    label: str
    "The label/name of the expression"
    kind: MeasurementKind
    "The type of metric data this expression represents"
    ontology: Optional[ID] = None
    "The ID of the ontology this expression belongs to. If not provided, uses default ontology"
    description: Optional[str] = None
    "A detailed description of the expression"
    purl: Optional[str] = None
    "Permanent URL identifier for the expression"
    color: Optional[Tuple[int, ...]] = None
    "RGBA color values as list of 3 or 4 integers"
    image: Optional[RemoteUpload] = None
    "An optional image associated with this expression"
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class StructureCategoryInput(BaseModel):
    """Input for creating a new expression"""

    ontology: Optional[ID] = None
    "The ID of the ontology this expression belongs to. If not provided, uses default ontology"
    identifier: StructureIdentifier
    "The label/name of the expression"
    description: Optional[str] = None
    "A detailed description of the expression"
    purl: Optional[str] = None
    "Permanent URL identifier for the expression"
    color: Optional[Tuple[int, ...]] = None
    "RGBA color values as list of 3 or 4 integers"
    image: Optional[RemoteUpload] = None
    "An optional image associated with this expression"
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class RelationCategoryInput(BaseModel):
    """Input for creating a new expression"""

    ontology: Optional[ID] = None
    "The ID of the ontology this expression belongs to. If not provided, uses default ontology"
    label: str
    "The label/name of the expression"
    description: Optional[str] = None
    "A detailed description of the expression"
    purl: Optional[str] = None
    "Permanent URL identifier for the expression"
    color: Optional[Tuple[int, ...]] = None
    "RGBA color values as list of 3 or 4 integers"
    image: Optional[RemoteUpload] = None
    "An optional image associated with this expression"
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class GenericCategoryInput(BaseModel):
    """Input for creating a new expression"""

    ontology: Optional[ID] = None
    "The ID of the ontology this expression belongs to. If not provided, uses default ontology"
    label: str
    "The label/name of the expression"
    description: Optional[str] = None
    "A detailed description of the expression"
    purl: Optional[str] = None
    "Permanent URL identifier for the expression"
    color: Optional[Tuple[int, ...]] = None
    "RGBA color values as list of 3 or 4 integers"
    image: Optional[RemoteUpload] = None
    "An optional image associated with this expression"
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class PairsPairsLeftBase(BaseModel):
    id: NodeID
    "The unique identifier of the entity within its graph"
    model_config = ConfigDict(frozen=True)


class PairsPairsLeftBaseEntity(PairsPairsLeftBase, BaseModel):
    typename: Literal["Entity"] = Field(
        alias="__typename", default="Entity", exclude=True
    )


class PairsPairsLeftBaseStructure(PairsPairsLeftBase, BaseModel):
    typename: Literal["Structure"] = Field(
        alias="__typename", default="Structure", exclude=True
    )


class PairsPairsRightBase(BaseModel):
    id: NodeID
    "The unique identifier of the entity within its graph"
    model_config = ConfigDict(frozen=True)


class PairsPairsRightBaseEntity(PairsPairsRightBase, BaseModel):
    typename: Literal["Entity"] = Field(
        alias="__typename", default="Entity", exclude=True
    )


class PairsPairsRightBaseStructure(PairsPairsRightBase, BaseModel):
    typename: Literal["Structure"] = Field(
        alias="__typename", default="Structure", exclude=True
    )


class PairsPairs(BaseModel):
    """A paired structure two entities and the relation between them."""

    typename: Literal["Pair"] = Field(alias="__typename", default="Pair", exclude=True)
    left: Annotated[
        Union[PairsPairsLeftBaseEntity, PairsPairsLeftBaseStructure],
        Field(discriminator="typename"),
    ]
    "The left entity."
    right: Annotated[
        Union[PairsPairsRightBaseEntity, PairsPairsRightBaseStructure],
        Field(discriminator="typename"),
    ]
    "The right entity."
    model_config = ConfigDict(frozen=True)


class Pairs(BaseModel):
    """A collection of paired entities."""

    typename: Literal["Pairs"] = Field(
        alias="__typename", default="Pairs", exclude=True
    )
    pairs: Tuple[PairsPairs, ...]
    "The paired entities."
    model_config = ConfigDict(frozen=True)


class TableColumns(BaseModel):
    """A column definition for a table view."""

    typename: Literal["Column"] = Field(
        alias="__typename", default="Column", exclude=True
    )
    name: str
    model_config = ConfigDict(frozen=True)


class Table(BaseModel):
    """A collection of paired entities."""

    typename: Literal["Table"] = Field(
        alias="__typename", default="Table", exclude=True
    )
    rows: Tuple[Any, ...]
    "The paired entities."
    columns: Tuple[TableColumns, ...]
    "The columns describind this table."
    model_config = ConfigDict(frozen=True)


class PresignedPostCredentials(BaseModel):
    """Temporary Credentials for a file upload that can be used by a Client (e.g. in a python datalayer)"""

    typename: Literal["PresignedPostCredentials"] = Field(
        alias="__typename", default="PresignedPostCredentials", exclude=True
    )
    key: str
    x_amz_credential: str = Field(alias="xAmzCredential")
    x_amz_algorithm: str = Field(alias="xAmzAlgorithm")
    x_amz_date: str = Field(alias="xAmzDate")
    x_amz_signature: str = Field(alias="xAmzSignature")
    policy: str
    datalayer: str
    bucket: str
    store: str
    model_config = ConfigDict(frozen=True)


class ListGraphQuery(BaseModel):
    """A view of a graph, that contains entities and relations."""

    typename: Literal["GraphQuery"] = Field(
        alias="__typename", default="GraphQuery", exclude=True
    )
    id: ID
    name: str
    query: str
    description: Optional[str] = Field(default=None)
    model_config = ConfigDict(frozen=True)


class GraphOntology(OntologyTrait, BaseModel):
    """An ontology represents a formal naming and definition of types, properties, and
    interrelationships between entities in a specific domain. In kraph, ontologies provide the vocabulary
    and semantic structure for organizing data across graphs."""

    typename: Literal["Ontology"] = Field(
        alias="__typename", default="Ontology", exclude=True
    )
    id: ID
    "The unique identifier of the ontology"
    model_config = ConfigDict(frozen=True)


class Graph(GraphTrait, BaseModel):
    """A graph, that contains entities and relations."""

    typename: Literal["Graph"] = Field(
        alias="__typename", default="Graph", exclude=True
    )
    id: ID
    name: str
    ontology: GraphOntology
    model_config = ConfigDict(frozen=True)


class ProtocolStepTemplate(BaseModel):
    typename: Literal["ProtocolStepTemplate"] = Field(
        alias="__typename", default="ProtocolStepTemplate", exclude=True
    )
    id: ID
    name: str
    model_config = ConfigDict(frozen=True)


class ProtocolStepReagentmappingsReagent(BaseModel):
    typename: Literal["Reagent"] = Field(
        alias="__typename", default="Reagent", exclude=True
    )
    id: ID
    model_config = ConfigDict(frozen=True)


class ProtocolStepReagentmappings(BaseModel):
    typename: Literal["ReagentMapping"] = Field(
        alias="__typename", default="ReagentMapping", exclude=True
    )
    reagent: ProtocolStepReagentmappingsReagent
    model_config = ConfigDict(frozen=True)


class ProtocolStepForreagent(BaseModel):
    typename: Literal["Reagent"] = Field(
        alias="__typename", default="Reagent", exclude=True
    )
    id: ID
    model_config = ConfigDict(frozen=True)


class ProtocolStep(BaseModel):
    typename: Literal["ProtocolStep"] = Field(
        alias="__typename", default="ProtocolStep", exclude=True
    )
    id: ID
    template: ProtocolStepTemplate
    reagent_mappings: Tuple[ProtocolStepReagentmappings, ...] = Field(
        alias="reagentMappings"
    )
    for_reagent: Optional[ProtocolStepForreagent] = Field(
        default=None, alias="forReagent"
    )
    model_config = ConfigDict(frozen=True)


class ScatterPlot(BaseModel):
    """A scatter plot of a table graph, that contains entities and relations."""

    typename: Literal["ScatterPlot"] = Field(
        alias="__typename", default="ScatterPlot", exclude=True
    )
    id: ID
    name: str
    model_config = ConfigDict(frozen=True)


class ListScatterPlot(BaseModel):
    """A scatter plot of a table graph, that contains entities and relations."""

    typename: Literal["ScatterPlot"] = Field(
        alias="__typename", default="ScatterPlot", exclude=True
    )
    id: ID
    name: str
    x_column: str = Field(alias="xColumn")
    y_column: str = Field(alias="yColumn")
    model_config = ConfigDict(frozen=True)


class ReagentExpression(BaseModel):
    typename: Literal["Expression"] = Field(
        alias="__typename", default="Expression", exclude=True
    )
    id: ID
    "The unique identifier of the expression within its graph"
    model_config = ConfigDict(frozen=True)


class Reagent(BaseModel):
    typename: Literal["Reagent"] = Field(
        alias="__typename", default="Reagent", exclude=True
    )
    id: ID
    expression: Optional[ReagentExpression] = Field(default=None)
    lot_id: str = Field(alias="lotId")
    model_config = ConfigDict(frozen=True)


class BaseEdgeBase(BaseModel):
    id: NodeID
    "The unique identifier of the entity within its graph"
    left_id: str = Field(alias="leftId")
    right_id: str = Field(alias="rightId")


class BaseEdgeCatch(BaseEdgeBase):
    typename: str = Field(alias="__typename", exclude=True)
    id: NodeID
    "The unique identifier of the entity within its graph"
    left_id: str = Field(alias="leftId")
    right_id: str = Field(alias="rightId")


class BaseEdgeRelation(BaseEdgeBase, BaseModel):
    typename: Literal["Relation"] = Field(
        alias="__typename", default="Relation", exclude=True
    )


class BaseEdgeMeasurement(BaseEdgeBase, BaseModel):
    typename: Literal["Measurement"] = Field(
        alias="__typename", default="Measurement", exclude=True
    )


class BaseEdgeComputedMeasurement(BaseEdgeBase, BaseModel):
    typename: Literal["ComputedMeasurement"] = Field(
        alias="__typename", default="ComputedMeasurement", exclude=True
    )


class MeasurementCategory(MeasurementCategoryTrait, BaseModel):
    typename: Literal["MeasurementCategory"] = Field(
        alias="__typename", default="MeasurementCategory", exclude=True
    )
    id: ID
    "The unique identifier of the expression within its graph"
    label: str
    "The unique identifier of the expression within its graph"
    metric_kind: MeasurementKind = Field(alias="metricKind")
    "The kind of metric this expression represents"
    model_config = ConfigDict(frozen=True)


class Measurement(BaseModel):
    """A measurement is an edge from a structure to an entity. Importantly Measurement are always directed from the structure to the entity, and never the other way around.

    Why an edge?
    Because a measurement is a relation between two entities, and it is important to keep track of the provenance of the data.
                     By making the measurement an edge, we can keep track of the timestamp when the data point (entity) was taken,
                      and the timestamp when the measurment was created. We can also keep track of the validity of the measurment
                     over time (valid_from, valid_to). Through these edges we can establish when a entity really existed (i.e. when it was measured)
    """

    typename: Literal["Measurement"] = Field(
        alias="__typename", default="Measurement", exclude=True
    )
    value: Any
    "The value of the measurement"
    category: MeasurementCategory
    model_config = ConfigDict(frozen=True)


class RelationCategory(RelationCategoryTrait, BaseModel):
    typename: Literal["RelationCategory"] = Field(
        alias="__typename", default="RelationCategory", exclude=True
    )
    id: ID
    "The unique identifier of the expression within its graph"
    label: str
    "The unique identifier of the expression within its graph"
    model_config = ConfigDict(frozen=True)


class Relation(BaseModel):
    """A relation is an edge between two entities. It is a directed edge, that connects two entities and established a relationship
    that is not a measurement between them. I.e. when they are an subjective assertion about the entities.



    """

    typename: Literal["Relation"] = Field(
        alias="__typename", default="Relation", exclude=True
    )
    category: RelationCategory
    model_config = ConfigDict(frozen=True)


class BaseCategoryBase(BaseModel):
    id: ID
    "The unique identifier of the expression within its graph"
    label: str
    "The unique identifier of the expression within its graph"
    age_name: str = Field(alias="ageName")
    "The unique identifier of the expression within its graph"


class BaseCategoryCatch(BaseCategoryBase):
    typename: str = Field(alias="__typename", exclude=True)
    id: ID
    "The unique identifier of the expression within its graph"
    label: str
    "The unique identifier of the expression within its graph"
    age_name: str = Field(alias="ageName")
    "The unique identifier of the expression within its graph"


class BaseCategoryStructureCategory(BaseCategoryBase, BaseModel):
    typename: Literal["StructureCategory"] = Field(
        alias="__typename", default="StructureCategory", exclude=True
    )


class BaseCategoryGenericCategory(BaseCategoryBase, BaseModel):
    typename: Literal["GenericCategory"] = Field(
        alias="__typename", default="GenericCategory", exclude=True
    )


class BaseCategoryMeasurementCategory(BaseCategoryBase, BaseModel):
    typename: Literal["MeasurementCategory"] = Field(
        alias="__typename", default="MeasurementCategory", exclude=True
    )


class BaseCategoryRelationCategory(BaseCategoryBase, BaseModel):
    typename: Literal["RelationCategory"] = Field(
        alias="__typename", default="RelationCategory", exclude=True
    )


class BaseNodeCategoryBase(BaseModel):
    id: ID
    "The unique identifier of the expression within its graph"


class BaseNodeCategoryCatch(BaseNodeCategoryBase):
    typename: str = Field(alias="__typename", exclude=True)
    id: ID
    "The unique identifier of the expression within its graph"


class BaseNodeCategoryStructureCategory(BaseNodeCategoryBase, BaseModel):
    typename: Literal["StructureCategory"] = Field(
        alias="__typename", default="StructureCategory", exclude=True
    )


class BaseNodeCategoryGenericCategory(BaseNodeCategoryBase, BaseModel):
    typename: Literal["GenericCategory"] = Field(
        alias="__typename", default="GenericCategory", exclude=True
    )


class BaseEdgeCategoryLeftBase(BaseModel):
    id: ID
    "The unique identifier of the expression within its graph"
    model_config = ConfigDict(frozen=True)


class BaseEdgeCategoryLeftBaseStructureCategory(BaseEdgeCategoryLeftBase, BaseModel):
    typename: Literal["StructureCategory"] = Field(
        alias="__typename", default="StructureCategory", exclude=True
    )


class BaseEdgeCategoryLeftBaseGenericCategory(BaseEdgeCategoryLeftBase, BaseModel):
    typename: Literal["GenericCategory"] = Field(
        alias="__typename", default="GenericCategory", exclude=True
    )


class BaseEdgeCategoryRightBase(BaseModel):
    id: ID
    "The unique identifier of the expression within its graph"
    model_config = ConfigDict(frozen=True)


class BaseEdgeCategoryRightBaseStructureCategory(BaseEdgeCategoryRightBase, BaseModel):
    typename: Literal["StructureCategory"] = Field(
        alias="__typename", default="StructureCategory", exclude=True
    )


class BaseEdgeCategoryRightBaseGenericCategory(BaseEdgeCategoryRightBase, BaseModel):
    typename: Literal["GenericCategory"] = Field(
        alias="__typename", default="GenericCategory", exclude=True
    )


class BaseEdgeCategoryBase(BaseModel):
    left: Optional[
        Annotated[
            Union[
                BaseEdgeCategoryLeftBaseStructureCategory,
                BaseEdgeCategoryLeftBaseGenericCategory,
            ],
            Field(discriminator="typename"),
        ]
    ] = Field(default=None)
    "The category of the left entity"
    right: Optional[
        Annotated[
            Union[
                BaseEdgeCategoryRightBaseStructureCategory,
                BaseEdgeCategoryRightBaseGenericCategory,
            ],
            Field(discriminator="typename"),
        ]
    ] = Field(default=None)
    "The category of the right entity"


class BaseEdgeCategoryCatch(BaseEdgeCategoryBase):
    typename: str = Field(alias="__typename", exclude=True)
    left: Optional[
        Annotated[
            Union[
                BaseEdgeCategoryLeftBaseStructureCategory,
                BaseEdgeCategoryLeftBaseGenericCategory,
            ],
            Field(discriminator="typename"),
        ]
    ] = Field(default=None)
    "The category of the left entity"
    right: Optional[
        Annotated[
            Union[
                BaseEdgeCategoryRightBaseStructureCategory,
                BaseEdgeCategoryRightBaseGenericCategory,
            ],
            Field(discriminator="typename"),
        ]
    ] = Field(default=None)
    "The category of the right entity"


class BaseEdgeCategoryMeasurementCategory(BaseEdgeCategoryBase, BaseModel):
    typename: Literal["MeasurementCategory"] = Field(
        alias="__typename", default="MeasurementCategory", exclude=True
    )


class BaseEdgeCategoryRelationCategory(BaseEdgeCategoryBase, BaseModel):
    typename: Literal["RelationCategory"] = Field(
        alias="__typename", default="RelationCategory", exclude=True
    )


class BaseListCategoryStore(HasPresignedDownloadAccessor, BaseModel):
    typename: Literal["MediaStore"] = Field(
        alias="__typename", default="MediaStore", exclude=True
    )
    presigned_url: str = Field(alias="presignedUrl")
    model_config = ConfigDict(frozen=True)


class BaseListCategoryBase(BaseModel):
    id: ID
    "The unique identifier of the expression within its graph"
    label: str
    "The unique identifier of the expression within its graph"
    description: Optional[str] = Field(default=None)
    "A description of the expression."
    age_name: str = Field(alias="ageName")
    "The unique identifier of the expression within its graph"
    store: Optional[BaseListCategoryStore] = Field(default=None)
    "An image or other media file that can be used to represent the expression."


class BaseListCategoryCatch(BaseListCategoryBase):
    typename: str = Field(alias="__typename", exclude=True)
    id: ID
    "The unique identifier of the expression within its graph"
    label: str
    "The unique identifier of the expression within its graph"
    description: Optional[str] = Field(default=None)
    "A description of the expression."
    age_name: str = Field(alias="ageName")
    "The unique identifier of the expression within its graph"
    store: Optional[BaseListCategoryStore] = Field(default=None)
    "An image or other media file that can be used to represent the expression."


class BaseListCategoryStructureCategory(BaseListCategoryBase, BaseModel):
    typename: Literal["StructureCategory"] = Field(
        alias="__typename", default="StructureCategory", exclude=True
    )


class BaseListCategoryGenericCategory(BaseListCategoryBase, BaseModel):
    typename: Literal["GenericCategory"] = Field(
        alias="__typename", default="GenericCategory", exclude=True
    )


class BaseListCategoryMeasurementCategory(BaseListCategoryBase, BaseModel):
    typename: Literal["MeasurementCategory"] = Field(
        alias="__typename", default="MeasurementCategory", exclude=True
    )


class BaseListCategoryRelationCategory(BaseListCategoryBase, BaseModel):
    typename: Literal["RelationCategory"] = Field(
        alias="__typename", default="RelationCategory", exclude=True
    )


class BaseListNodeCategoryBase(BaseModel):
    id: ID
    "The unique identifier of the expression within its graph"


class BaseListNodeCategoryCatch(BaseListNodeCategoryBase):
    typename: str = Field(alias="__typename", exclude=True)
    id: ID
    "The unique identifier of the expression within its graph"


class BaseListNodeCategoryStructureCategory(BaseListNodeCategoryBase, BaseModel):
    typename: Literal["StructureCategory"] = Field(
        alias="__typename", default="StructureCategory", exclude=True
    )


class BaseListNodeCategoryGenericCategory(BaseListNodeCategoryBase, BaseModel):
    typename: Literal["GenericCategory"] = Field(
        alias="__typename", default="GenericCategory", exclude=True
    )


class BaseListEdgeCategoryLeftBase(BaseModel):
    id: ID
    "The unique identifier of the expression within its graph"
    model_config = ConfigDict(frozen=True)


class BaseListEdgeCategoryLeftBaseStructureCategory(
    BaseListEdgeCategoryLeftBase, BaseModel
):
    typename: Literal["StructureCategory"] = Field(
        alias="__typename", default="StructureCategory", exclude=True
    )


class BaseListEdgeCategoryLeftBaseGenericCategory(
    BaseListEdgeCategoryLeftBase, BaseModel
):
    typename: Literal["GenericCategory"] = Field(
        alias="__typename", default="GenericCategory", exclude=True
    )


class BaseListEdgeCategoryRightBase(BaseModel):
    id: ID
    "The unique identifier of the expression within its graph"
    model_config = ConfigDict(frozen=True)


class BaseListEdgeCategoryRightBaseStructureCategory(
    BaseListEdgeCategoryRightBase, BaseModel
):
    typename: Literal["StructureCategory"] = Field(
        alias="__typename", default="StructureCategory", exclude=True
    )


class BaseListEdgeCategoryRightBaseGenericCategory(
    BaseListEdgeCategoryRightBase, BaseModel
):
    typename: Literal["GenericCategory"] = Field(
        alias="__typename", default="GenericCategory", exclude=True
    )


class BaseListEdgeCategoryBase(BaseModel):
    left: Optional[
        Annotated[
            Union[
                BaseListEdgeCategoryLeftBaseStructureCategory,
                BaseListEdgeCategoryLeftBaseGenericCategory,
            ],
            Field(discriminator="typename"),
        ]
    ] = Field(default=None)
    "The category of the left entity"
    right: Optional[
        Annotated[
            Union[
                BaseListEdgeCategoryRightBaseStructureCategory,
                BaseListEdgeCategoryRightBaseGenericCategory,
            ],
            Field(discriminator="typename"),
        ]
    ] = Field(default=None)
    "The category of the right entity"


class BaseListEdgeCategoryCatch(BaseListEdgeCategoryBase):
    typename: str = Field(alias="__typename", exclude=True)
    left: Optional[
        Annotated[
            Union[
                BaseListEdgeCategoryLeftBaseStructureCategory,
                BaseListEdgeCategoryLeftBaseGenericCategory,
            ],
            Field(discriminator="typename"),
        ]
    ] = Field(default=None)
    "The category of the left entity"
    right: Optional[
        Annotated[
            Union[
                BaseListEdgeCategoryRightBaseStructureCategory,
                BaseListEdgeCategoryRightBaseGenericCategory,
            ],
            Field(discriminator="typename"),
        ]
    ] = Field(default=None)
    "The category of the right entity"


class BaseListEdgeCategoryMeasurementCategory(BaseListEdgeCategoryBase, BaseModel):
    typename: Literal["MeasurementCategory"] = Field(
        alias="__typename", default="MeasurementCategory", exclude=True
    )


class BaseListEdgeCategoryRelationCategory(BaseListEdgeCategoryBase, BaseModel):
    typename: Literal["RelationCategory"] = Field(
        alias="__typename", default="RelationCategory", exclude=True
    )


class MediaStore(HasPresignedDownloadAccessor, BaseModel):
    typename: Literal["MediaStore"] = Field(
        alias="__typename", default="MediaStore", exclude=True
    )
    id: ID
    presigned_url: str = Field(alias="presignedUrl")
    key: str
    model_config = ConfigDict(frozen=True)


class BaseNodeBase(BaseModel):
    id: NodeID
    "The unique identifier of the entity within its graph"
    label: str


class BaseNodeCatch(BaseNodeBase):
    typename: str = Field(alias="__typename", exclude=True)
    id: NodeID
    "The unique identifier of the entity within its graph"
    label: str


class BaseNodeEntity(BaseNodeBase, BaseModel):
    typename: Literal["Entity"] = Field(
        alias="__typename", default="Entity", exclude=True
    )


class BaseNodeStructure(BaseNodeBase, BaseModel):
    typename: Literal["Structure"] = Field(
        alias="__typename", default="Structure", exclude=True
    )


class EntityCategory(GenericCategoryTrait, BaseModel):
    typename: Literal["GenericCategory"] = Field(
        alias="__typename", default="GenericCategory", exclude=True
    )
    id: ID
    "The unique identifier of the expression within its graph"
    label: str
    "The unique identifier of the expression within its graph"
    model_config = ConfigDict(frozen=True)


class Entity(EntityTrait, BaseModel):
    """A Entity is a recorded data point in a graph. It can measure a property of an entity through a direct measurement edge, that connects the entity to the structure. It of course can relate to other structures through relation edges."""

    typename: Literal["Entity"] = Field(
        alias="__typename", default="Entity", exclude=True
    )
    id: NodeID
    "The unique identifier of the entity within its graph"
    category: EntityCategory
    "Protocol steps where this entity was the target"
    model_config = ConfigDict(frozen=True)


class Structure(StructureTrait, BaseModel):
    """A Structure is a recorded data point in a graph. It can measure a property of an entity through a direct measurement edge, that connects the entity to the structure. It of course can relate to other structures through relation edges."""

    typename: Literal["Structure"] = Field(
        alias="__typename", default="Structure", exclude=True
    )
    id: NodeID
    "The unique identifier of the entity within its graph"
    object: str
    "The expression that defines this entity's type"
    identifier: str
    "The unique identifier of the entity within its graph"
    model_config = ConfigDict(frozen=True)


class GraphQuery(BaseModel):
    """A view of a graph, that contains entities and relations."""

    typename: Literal["GraphQuery"] = Field(
        alias="__typename", default="GraphQuery", exclude=True
    )
    id: ID
    name: str
    scatter_plots: Tuple[ListScatterPlot, ...] = Field(alias="scatterPlots")
    model_config = ConfigDict(frozen=True)


class EdgeBase(BaseModel):
    pass


class EdgeCatch(EdgeBase):
    typename: str = Field(alias="__typename", exclude=True)


class EdgeRelation(BaseEdgeRelation, Relation, EdgeBase, BaseModel):
    typename: Literal["Relation"] = Field(
        alias="__typename", default="Relation", exclude=True
    )


class EdgeMeasurement(BaseEdgeMeasurement, Measurement, EdgeBase, BaseModel):
    typename: Literal["Measurement"] = Field(
        alias="__typename", default="Measurement", exclude=True
    )


class EdgeComputedMeasurement(BaseEdgeComputedMeasurement, EdgeBase, BaseModel):
    typename: Literal["ComputedMeasurement"] = Field(
        alias="__typename", default="ComputedMeasurement", exclude=True
    )


class StructureCategory(
    BaseNodeCategoryStructureCategory,
    BaseCategoryStructureCategory,
    StructureCategoryTrait,
    BaseModel,
):
    typename: Literal["StructureCategory"] = Field(
        alias="__typename", default="StructureCategory", exclude=True
    )
    identifier: str
    "The structure that this class represents"
    model_config = ConfigDict(frozen=True)


class GenericCategory(
    BaseNodeCategoryGenericCategory,
    BaseCategoryGenericCategory,
    GenericCategoryTrait,
    BaseModel,
):
    typename: Literal["GenericCategory"] = Field(
        alias="__typename", default="GenericCategory", exclude=True
    )
    instance_kind: InstanceKind = Field(alias="instanceKind")
    "The kind of instance this expression creates"
    model_config = ConfigDict(frozen=True)


class MeasurementCategory(
    BaseEdgeCategoryMeasurementCategory,
    BaseCategoryMeasurementCategory,
    MeasurementCategoryTrait,
    BaseModel,
):
    typename: Literal["MeasurementCategory"] = Field(
        alias="__typename", default="MeasurementCategory", exclude=True
    )
    metric_kind: MeasurementKind = Field(alias="metricKind")
    "The kind of metric this expression represents"
    model_config = ConfigDict(frozen=True)


class RelationCategory(
    BaseEdgeCategoryRelationCategory,
    BaseCategoryRelationCategory,
    RelationCategoryTrait,
    BaseModel,
):
    typename: Literal["RelationCategory"] = Field(
        alias="__typename", default="RelationCategory", exclude=True
    )
    model_config = ConfigDict(frozen=True)


class ListGenericCategory(
    BaseNodeCategoryGenericCategory,
    BaseListCategoryGenericCategory,
    GenericCategoryTrait,
    BaseModel,
):
    typename: Literal["GenericCategory"] = Field(
        alias="__typename", default="GenericCategory", exclude=True
    )
    instance_kind: InstanceKind = Field(alias="instanceKind")
    "The kind of instance this expression creates"
    model_config = ConfigDict(frozen=True)


class ListStructureCategory(
    BaseListNodeCategoryStructureCategory,
    BaseListCategoryStructureCategory,
    StructureCategoryTrait,
    BaseModel,
):
    typename: Literal["StructureCategory"] = Field(
        alias="__typename", default="StructureCategory", exclude=True
    )
    identifier: str
    "The structure that this class represents"
    model_config = ConfigDict(frozen=True)


class ListMeasurementCategory(
    BaseListEdgeCategoryMeasurementCategory,
    BaseListCategoryMeasurementCategory,
    MeasurementCategoryTrait,
    BaseModel,
):
    typename: Literal["MeasurementCategory"] = Field(
        alias="__typename", default="MeasurementCategory", exclude=True
    )
    metric_kind: MeasurementKind = Field(alias="metricKind")
    "The kind of metric this expression represents"
    model_config = ConfigDict(frozen=True)


class ListRelationCategory(
    BaseListEdgeCategoryRelationCategory,
    BaseListCategoryRelationCategory,
    RelationCategoryTrait,
    BaseModel,
):
    typename: Literal["RelationCategory"] = Field(
        alias="__typename", default="RelationCategory", exclude=True
    )
    model_config = ConfigDict(frozen=True)


class Model(BaseModel):
    """A model represents a trained machine learning model that can be used for analysis."""

    typename: Literal["Model"] = Field(
        alias="__typename", default="Model", exclude=True
    )
    id: ID
    "The unique identifier of the model"
    name: str
    "The name of the model"
    store: Optional[MediaStore] = Field(default=None)
    "Optional file storage location containing the model weights/parameters"
    model_config = ConfigDict(frozen=True)


class NodeBase(BaseModel):
    pass


class NodeCatch(NodeBase):
    typename: str = Field(alias="__typename", exclude=True)


class NodeEntity(BaseNodeEntity, Entity, NodeBase, BaseModel):
    typename: Literal["Entity"] = Field(
        alias="__typename", default="Entity", exclude=True
    )


class NodeStructure(BaseNodeStructure, Structure, NodeBase, BaseModel):
    typename: Literal["Structure"] = Field(
        alias="__typename", default="Structure", exclude=True
    )


class NodeCategoryBase(BaseModel):
    pass


class NodeCategoryCatch(NodeCategoryBase):
    typename: str = Field(alias="__typename", exclude=True)


class NodeCategoryStructureCategory(StructureCategory, NodeCategoryBase, BaseModel):
    typename: Literal["StructureCategory"] = Field(
        alias="__typename", default="StructureCategory", exclude=True
    )


class NodeCategoryGenericCategory(GenericCategory, NodeCategoryBase, BaseModel):
    typename: Literal["GenericCategory"] = Field(
        alias="__typename", default="GenericCategory", exclude=True
    )


class Ontology(OntologyTrait, BaseModel):
    """An ontology represents a formal naming and definition of types, properties, and
    interrelationships between entities in a specific domain. In kraph, ontologies provide the vocabulary
    and semantic structure for organizing data across graphs."""

    typename: Literal["Ontology"] = Field(
        alias="__typename", default="Ontology", exclude=True
    )
    id: ID
    "The unique identifier of the ontology"
    name: str
    "The name of the ontology"
    structure_categories: Tuple[ListStructureCategory, ...] = Field(
        alias="structureCategories"
    )
    "The list of structure expressions defined in this ontology"
    generic_categories: Tuple[ListGenericCategory, ...] = Field(
        alias="genericCategories"
    )
    "The list of generic expressions defined in this ontology"
    relation_categories: Tuple[ListRelationCategory, ...] = Field(
        alias="relationCategories"
    )
    "The list of relation expressions defined in this ontology"
    measurement_categories: Tuple[ListMeasurementCategory, ...] = Field(
        alias="measurementCategories"
    )
    "The list of measurement exprdessions defined in this ontology"
    graph_queries: Tuple[ListGraphQuery, ...] = Field(alias="graphQueries")
    "The list of graph queries defined in this ontology"
    model_config = ConfigDict(frozen=True)


class PathNodesBase(BaseModel):
    pass
    model_config = ConfigDict(frozen=True)


class PathNodesBaseEntity(NodeEntity, PathNodesBase, BaseModel):
    typename: Literal["Entity"] = Field(
        alias="__typename", default="Entity", exclude=True
    )


class PathNodesBaseStructure(NodeStructure, PathNodesBase, BaseModel):
    typename: Literal["Structure"] = Field(
        alias="__typename", default="Structure", exclude=True
    )


class PathEdgesBase(BaseModel):
    pass
    model_config = ConfigDict(frozen=True)


class PathEdgesBaseRelation(EdgeRelation, PathEdgesBase, BaseModel):
    typename: Literal["Relation"] = Field(
        alias="__typename", default="Relation", exclude=True
    )


class PathEdgesBaseMeasurement(EdgeMeasurement, PathEdgesBase, BaseModel):
    typename: Literal["Measurement"] = Field(
        alias="__typename", default="Measurement", exclude=True
    )


class PathEdgesBaseComputedMeasurement(
    EdgeComputedMeasurement, PathEdgesBase, BaseModel
):
    typename: Literal["ComputedMeasurement"] = Field(
        alias="__typename", default="ComputedMeasurement", exclude=True
    )


class Path(BaseModel):
    typename: Literal["Path"] = Field(alias="__typename", default="Path", exclude=True)
    nodes: Tuple[
        Annotated[
            Union[PathNodesBaseEntity, PathNodesBaseStructure],
            Field(discriminator="typename"),
        ],
        ...,
    ]
    edges: Tuple[
        Annotated[
            Union[
                PathEdgesBaseRelation,
                PathEdgesBaseMeasurement,
                PathEdgesBaseComputedMeasurement,
            ],
            Field(discriminator="typename"),
        ],
        ...,
    ]
    model_config = ConfigDict(frozen=True)


class NodeViewQuery(BaseModel):
    """A view of a node entities and relations."""

    typename: Literal["NodeQuery"] = Field(
        alias="__typename", default="NodeQuery", exclude=True
    )
    id: ID
    name: str
    model_config = ConfigDict(frozen=True)


class NodeView(BaseModel):
    """A view of a graph, that contains entities and relations."""

    typename: Literal["NodeView"] = Field(
        alias="__typename", default="NodeView", exclude=True
    )
    id: ID
    query: NodeViewQuery
    render: Union[Path, Pairs, Table]
    model_config = ConfigDict(frozen=True)


class GraphViewQuery(BaseModel):
    """A view of a graph, that contains entities and relations."""

    typename: Literal["GraphQuery"] = Field(
        alias="__typename", default="GraphQuery", exclude=True
    )
    id: ID
    name: str
    model_config = ConfigDict(frozen=True)


class GraphView(BaseModel):
    """A view of a graph, that contains entities and relations."""

    typename: Literal["GraphView"] = Field(
        alias="__typename", default="GraphView", exclude=True
    )
    id: ID
    query: GraphViewQuery
    render: Union[Path, Pairs, Table]
    model_config = ConfigDict(frozen=True)


class PlotView(BaseModel):
    """A view of a graph, that contains entities and relations."""

    typename: Literal["PlotView"] = Field(
        alias="__typename", default="PlotView", exclude=True
    )
    view: GraphView
    plot: ScatterPlot
    model_config = ConfigDict(frozen=True)


class CreateModelMutation(BaseModel):
    create_model: Model = Field(alias="createModel")
    "Create a new model"

    class Arguments(BaseModel):
        input: CreateModelInput

    class Meta:
        document = "fragment MediaStore on MediaStore {\n  id\n  presignedUrl\n  key\n  __typename\n}\n\nfragment Model on Model {\n  id\n  name\n  store {\n    ...MediaStore\n    __typename\n  }\n  __typename\n}\n\nmutation CreateModel($input: CreateModelInput!) {\n  createModel(input: $input) {\n    ...Model\n    __typename\n  }\n}"


class CreateGraphQueryMutationCreategraphquery(BaseModel):
    """A view of a graph, that contains entities and relations."""

    typename: Literal["GraphQuery"] = Field(
        alias="__typename", default="GraphQuery", exclude=True
    )
    id: ID
    name: str
    model_config = ConfigDict(frozen=True)


class CreateGraphQueryMutation(BaseModel):
    create_graph_query: CreateGraphQueryMutationCreategraphquery = Field(
        alias="createGraphQuery"
    )
    "Create a new graph query"

    class Arguments(BaseModel):
        input: GraphQueryInput

    class Meta:
        document = "mutation CreateGraphQuery($input: GraphQueryInput!) {\n  createGraphQuery(input: $input) {\n    id\n    name\n    __typename\n  }\n}"


class CreatePlotViewMutation(BaseModel):
    create_plot_view: PlotView = Field(alias="createPlotView")
    "Create a new plot view"

    class Arguments(BaseModel):
        input: PlotViewInput

    class Meta:
        document = "fragment BaseNode on Node {\n  id\n  label\n  __typename\n}\n\nfragment Entity on Entity {\n  id\n  category {\n    id\n    label\n    __typename\n  }\n  __typename\n}\n\nfragment BaseEdge on Edge {\n  id\n  leftId\n  rightId\n  __typename\n}\n\nfragment Relation on Relation {\n  category {\n    id\n    label\n    __typename\n  }\n  __typename\n}\n\nfragment Structure on Structure {\n  id\n  object\n  identifier\n  __typename\n}\n\nfragment Measurement on Measurement {\n  value\n  category {\n    id\n    label\n    metricKind\n    __typename\n  }\n  __typename\n}\n\nfragment Edge on Edge {\n  ...BaseEdge\n  ...Measurement\n  ...Relation\n  __typename\n}\n\nfragment Node on Node {\n  ...BaseNode\n  ...Entity\n  ...Structure\n  __typename\n}\n\nfragment Table on Table {\n  rows\n  columns {\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment Path on Path {\n  nodes {\n    ...Node\n    __typename\n  }\n  edges {\n    ...Edge\n    __typename\n  }\n  __typename\n}\n\nfragment Pairs on Pairs {\n  pairs {\n    left {\n      id\n      __typename\n    }\n    right {\n      id\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment GraphView on GraphView {\n  id\n  query {\n    id\n    name\n    __typename\n  }\n  render {\n    ...Path\n    ...Pairs\n    ...Table\n    __typename\n  }\n  __typename\n}\n\nfragment ScatterPlot on ScatterPlot {\n  id\n  name\n  __typename\n}\n\nfragment PlotView on PlotView {\n  view {\n    ...GraphView\n    __typename\n  }\n  plot {\n    ...ScatterPlot\n    __typename\n  }\n  __typename\n}\n\nmutation CreatePlotView($input: PlotViewInput!) {\n  createPlotView(input: $input) {\n    ...PlotView\n    __typename\n  }\n}"


class CreateGraphMutation(BaseModel):
    create_graph: Graph = Field(alias="createGraph")
    "Create a new graph"

    class Arguments(BaseModel):
        input: GraphInput

    class Meta:
        document = "fragment Graph on Graph {\n  id\n  name\n  ontology {\n    id\n    __typename\n  }\n  __typename\n}\n\nmutation CreateGraph($input: GraphInput!) {\n  createGraph(input: $input) {\n    ...Graph\n    __typename\n  }\n}"


class RequestUploadMutation(BaseModel):
    request_upload: PresignedPostCredentials = Field(alias="requestUpload")
    "Request a new file upload"

    class Arguments(BaseModel):
        input: RequestMediaUploadInput

    class Meta:
        document = "fragment PresignedPostCredentials on PresignedPostCredentials {\n  key\n  xAmzCredential\n  xAmzAlgorithm\n  xAmzDate\n  xAmzSignature\n  policy\n  datalayer\n  bucket\n  store\n  __typename\n}\n\nmutation RequestUpload($input: RequestMediaUploadInput!) {\n  requestUpload(input: $input) {\n    ...PresignedPostCredentials\n    __typename\n  }\n}"


class CreateProtocolStepMutation(BaseModel):
    create_protocol_step: ProtocolStep = Field(alias="createProtocolStep")
    "Create a new protocol step"

    class Arguments(BaseModel):
        input: ProtocolStepInput

    class Meta:
        document = "fragment ProtocolStep on ProtocolStep {\n  id\n  template {\n    id\n    name\n    __typename\n  }\n  reagentMappings {\n    reagent {\n      id\n      __typename\n    }\n    __typename\n  }\n  forReagent {\n    id\n    __typename\n  }\n  __typename\n}\n\nmutation CreateProtocolStep($input: ProtocolStepInput!) {\n  createProtocolStep(input: $input) {\n    ...ProtocolStep\n    __typename\n  }\n}"


class CreateScatterPlotMutation(BaseModel):
    create_scatter_plot: ScatterPlot = Field(alias="createScatterPlot")
    "Create a new scatter plot"

    class Arguments(BaseModel):
        input: ScatterPlotInput

    class Meta:
        document = "fragment ScatterPlot on ScatterPlot {\n  id\n  name\n  __typename\n}\n\nmutation CreateScatterPlot($input: ScatterPlotInput!) {\n  createScatterPlot(input: $input) {\n    ...ScatterPlot\n    __typename\n  }\n}"


class CreateNodeViewMutation(BaseModel):
    create_node_view: NodeView = Field(alias="createNodeView")
    "Create a new node view"

    class Arguments(BaseModel):
        input: NodeViewInput

    class Meta:
        document = "fragment BaseNode on Node {\n  id\n  label\n  __typename\n}\n\nfragment Entity on Entity {\n  id\n  category {\n    id\n    label\n    __typename\n  }\n  __typename\n}\n\nfragment BaseEdge on Edge {\n  id\n  leftId\n  rightId\n  __typename\n}\n\nfragment Relation on Relation {\n  category {\n    id\n    label\n    __typename\n  }\n  __typename\n}\n\nfragment Structure on Structure {\n  id\n  object\n  identifier\n  __typename\n}\n\nfragment Measurement on Measurement {\n  value\n  category {\n    id\n    label\n    metricKind\n    __typename\n  }\n  __typename\n}\n\nfragment Edge on Edge {\n  ...BaseEdge\n  ...Measurement\n  ...Relation\n  __typename\n}\n\nfragment Node on Node {\n  ...BaseNode\n  ...Entity\n  ...Structure\n  __typename\n}\n\nfragment Pairs on Pairs {\n  pairs {\n    left {\n      id\n      __typename\n    }\n    right {\n      id\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment Table on Table {\n  rows\n  columns {\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment Path on Path {\n  nodes {\n    ...Node\n    __typename\n  }\n  edges {\n    ...Edge\n    __typename\n  }\n  __typename\n}\n\nfragment NodeView on NodeView {\n  id\n  query {\n    id\n    name\n    __typename\n  }\n  render {\n    ...Path\n    ...Pairs\n    ...Table\n    __typename\n  }\n  __typename\n}\n\nmutation CreateNodeView($input: NodeViewInput!) {\n  createNodeView(input: $input) {\n    ...NodeView\n    __typename\n  }\n}"


class CreateNodeQueryMutationCreatenodequery(BaseModel):
    """A view of a node entities and relations."""

    typename: Literal["NodeQuery"] = Field(
        alias="__typename", default="NodeQuery", exclude=True
    )
    id: ID
    name: str
    model_config = ConfigDict(frozen=True)


class CreateNodeQueryMutation(BaseModel):
    create_node_query: CreateNodeQueryMutationCreatenodequery = Field(
        alias="createNodeQuery"
    )
    "Create a new node query"

    class Arguments(BaseModel):
        input: NodeQueryInput

    class Meta:
        document = "mutation CreateNodeQuery($input: NodeQueryInput!) {\n  createNodeQuery(input: $input) {\n    id\n    name\n    __typename\n  }\n}"


class CreateRelationMutation(BaseModel):
    create_relation: Relation = Field(alias="createRelation")
    "Create a new relation between entities"

    class Arguments(BaseModel):
        input: RelationInput

    class Meta:
        document = "fragment Relation on Relation {\n  category {\n    id\n    label\n    __typename\n  }\n  __typename\n}\n\nmutation CreateRelation($input: RelationInput!) {\n  createRelation(input: $input) {\n    ...Relation\n    __typename\n  }\n}"


class CreateReagentMutation(BaseModel):
    create_reagent: Reagent = Field(alias="createReagent")
    "Create a new reagent"

    class Arguments(BaseModel):
        input: ReagentInput

    class Meta:
        document = "fragment Reagent on Reagent {\n  id\n  expression {\n    id\n    __typename\n  }\n  lotId\n  __typename\n}\n\nmutation CreateReagent($input: ReagentInput!) {\n  createReagent(input: $input) {\n    ...Reagent\n    __typename\n  }\n}"


class CreateEntityMutation(BaseModel):
    create_entity: Entity = Field(alias="createEntity")
    "Create a new entity"

    class Arguments(BaseModel):
        input: EntityInput

    class Meta:
        document = "fragment Entity on Entity {\n  id\n  category {\n    id\n    label\n    __typename\n  }\n  __typename\n}\n\nmutation CreateEntity($input: EntityInput!) {\n  createEntity(input: $input) {\n    ...Entity\n    __typename\n  }\n}"


class CreateStructureMutation(BaseModel):
    create_structure: Structure = Field(alias="createStructure")
    "Create a new structure"

    class Arguments(BaseModel):
        input: StructureInput

    class Meta:
        document = "fragment Structure on Structure {\n  id\n  object\n  identifier\n  __typename\n}\n\nmutation CreateStructure($input: StructureInput!) {\n  createStructure(input: $input) {\n    ...Structure\n    __typename\n  }\n}"


class CreateGraphViewMutation(BaseModel):
    create_graph_view: GraphView = Field(alias="createGraphView")
    "Create a new graph view"

    class Arguments(BaseModel):
        input: GraphViewInput

    class Meta:
        document = "fragment BaseNode on Node {\n  id\n  label\n  __typename\n}\n\nfragment Entity on Entity {\n  id\n  category {\n    id\n    label\n    __typename\n  }\n  __typename\n}\n\nfragment BaseEdge on Edge {\n  id\n  leftId\n  rightId\n  __typename\n}\n\nfragment Relation on Relation {\n  category {\n    id\n    label\n    __typename\n  }\n  __typename\n}\n\nfragment Structure on Structure {\n  id\n  object\n  identifier\n  __typename\n}\n\nfragment Measurement on Measurement {\n  value\n  category {\n    id\n    label\n    metricKind\n    __typename\n  }\n  __typename\n}\n\nfragment Edge on Edge {\n  ...BaseEdge\n  ...Measurement\n  ...Relation\n  __typename\n}\n\nfragment Node on Node {\n  ...BaseNode\n  ...Entity\n  ...Structure\n  __typename\n}\n\nfragment Pairs on Pairs {\n  pairs {\n    left {\n      id\n      __typename\n    }\n    right {\n      id\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment Table on Table {\n  rows\n  columns {\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment Path on Path {\n  nodes {\n    ...Node\n    __typename\n  }\n  edges {\n    ...Edge\n    __typename\n  }\n  __typename\n}\n\nfragment GraphView on GraphView {\n  id\n  query {\n    id\n    name\n    __typename\n  }\n  render {\n    ...Path\n    ...Pairs\n    ...Table\n    __typename\n  }\n  __typename\n}\n\nmutation CreateGraphView($input: GraphViewInput!) {\n  createGraphView(input: $input) {\n    ...GraphView\n    __typename\n  }\n}"


class CreateMeasurementCategoryMutation(BaseModel):
    create_measurement_category: MeasurementCategory = Field(
        alias="createMeasurementCategory"
    )
    "Create a new expression"

    class Arguments(BaseModel):
        input: MeasurementCategoryInput

    class Meta:
        document = "fragment BaseCategory on Category {\n  id\n  label\n  ageName\n  __typename\n}\n\nfragment BaseEdgeCategory on EdgeCategory {\n  left {\n    id\n    __typename\n  }\n  right {\n    id\n    __typename\n  }\n  __typename\n}\n\nfragment MeasurementCategory on MeasurementCategory {\n  ...BaseCategory\n  ...BaseEdgeCategory\n  metricKind\n  __typename\n}\n\nmutation CreateMeasurementCategory($input: MeasurementCategoryInput!) {\n  createMeasurementCategory(input: $input) {\n    ...MeasurementCategory\n    __typename\n  }\n}"


class CreateStructureCategoryMutation(BaseModel):
    create_structure_category: StructureCategory = Field(
        alias="createStructureCategory"
    )
    "Create a new expression"

    class Arguments(BaseModel):
        input: StructureCategoryInput

    class Meta:
        document = "fragment BaseCategory on Category {\n  id\n  label\n  ageName\n  __typename\n}\n\nfragment BaseNodeCategory on NodeCategory {\n  id\n  __typename\n}\n\nfragment StructureCategory on StructureCategory {\n  ...BaseCategory\n  ...BaseNodeCategory\n  identifier\n  __typename\n}\n\nmutation CreateStructureCategory($input: StructureCategoryInput!) {\n  createStructureCategory(input: $input) {\n    ...StructureCategory\n    __typename\n  }\n}"


class CreateGenericCategoryMutation(BaseModel):
    create_generic_category: GenericCategory = Field(alias="createGenericCategory")
    "Create a new expression"

    class Arguments(BaseModel):
        input: GenericCategoryInput

    class Meta:
        document = "fragment BaseCategory on Category {\n  id\n  label\n  ageName\n  __typename\n}\n\nfragment BaseNodeCategory on NodeCategory {\n  id\n  __typename\n}\n\nfragment GenericCategory on GenericCategory {\n  ...BaseCategory\n  ...BaseNodeCategory\n  instanceKind\n  __typename\n}\n\nmutation CreateGenericCategory($input: GenericCategoryInput!) {\n  createGenericCategory(input: $input) {\n    ...GenericCategory\n    __typename\n  }\n}"


class CreateRelationCategoryMutation(BaseModel):
    create_relation_category: RelationCategory = Field(alias="createRelationCategory")
    "Create a new expression"

    class Arguments(BaseModel):
        input: RelationCategoryInput

    class Meta:
        document = "fragment BaseCategory on Category {\n  id\n  label\n  ageName\n  __typename\n}\n\nfragment BaseEdgeCategory on EdgeCategory {\n  left {\n    id\n    __typename\n  }\n  right {\n    id\n    __typename\n  }\n  __typename\n}\n\nfragment RelationCategory on RelationCategory {\n  ...BaseCategory\n  ...BaseEdgeCategory\n  __typename\n}\n\nmutation CreateRelationCategory($input: RelationCategoryInput!) {\n  createRelationCategory(input: $input) {\n    ...RelationCategory\n    __typename\n  }\n}"


class CreateMeasurementMutation(BaseModel):
    create_measurement: Measurement = Field(alias="createMeasurement")
    "Create a new metric for an entity"

    class Arguments(BaseModel):
        input: MeasurementInput

    class Meta:
        document = "fragment Measurement on Measurement {\n  value\n  category {\n    id\n    label\n    metricKind\n    __typename\n  }\n  __typename\n}\n\nmutation CreateMeasurement($input: MeasurementInput!) {\n  createMeasurement(input: $input) {\n    ...Measurement\n    __typename\n  }\n}"


class CreateOntologyMutation(BaseModel):
    create_ontology: Ontology = Field(alias="createOntology")
    "Create a new ontology"

    class Arguments(BaseModel):
        input: OntologyInput

    class Meta:
        document = "fragment BaseNodeCategory on NodeCategory {\n  id\n  __typename\n}\n\nfragment BaseListEdgeCategory on EdgeCategory {\n  left {\n    id\n    __typename\n  }\n  right {\n    id\n    __typename\n  }\n  __typename\n}\n\nfragment BaseListCategory on Category {\n  id\n  label\n  description\n  ageName\n  store {\n    presignedUrl\n    __typename\n  }\n  __typename\n}\n\nfragment BaseListNodeCategory on NodeCategory {\n  id\n  __typename\n}\n\nfragment ListGraphQuery on GraphQuery {\n  id\n  name\n  query\n  description\n  __typename\n}\n\nfragment ListGenericCategory on GenericCategory {\n  ...BaseListCategory\n  ...BaseNodeCategory\n  instanceKind\n  __typename\n}\n\nfragment ListMeasurementCategory on MeasurementCategory {\n  ...BaseListCategory\n  ...BaseListEdgeCategory\n  metricKind\n  __typename\n}\n\nfragment ListStructureCategory on StructureCategory {\n  ...BaseListCategory\n  ...BaseListNodeCategory\n  identifier\n  __typename\n}\n\nfragment ListRelationCategory on RelationCategory {\n  ...BaseListCategory\n  ...BaseListEdgeCategory\n  __typename\n}\n\nfragment Ontology on Ontology {\n  id\n  name\n  structureCategories {\n    ...ListStructureCategory\n    __typename\n  }\n  genericCategories {\n    ...ListGenericCategory\n    __typename\n  }\n  relationCategories {\n    ...ListRelationCategory\n    __typename\n  }\n  measurementCategories {\n    ...ListMeasurementCategory\n    __typename\n  }\n  graphQueries {\n    ...ListGraphQuery\n    __typename\n  }\n  __typename\n}\n\nmutation CreateOntology($input: OntologyInput!) {\n  createOntology(input: $input) {\n    ...Ontology\n    __typename\n  }\n}"


class GetRelationCategoryQuery(BaseModel):
    relation_category: RelationCategory = Field(alias="relationCategory")

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment BaseCategory on Category {\n  id\n  label\n  ageName\n  __typename\n}\n\nfragment BaseEdgeCategory on EdgeCategory {\n  left {\n    id\n    __typename\n  }\n  right {\n    id\n    __typename\n  }\n  __typename\n}\n\nfragment RelationCategory on RelationCategory {\n  ...BaseCategory\n  ...BaseEdgeCategory\n  __typename\n}\n\nquery GetRelationCategory($id: ID!) {\n  relationCategory(id: $id) {\n    ...RelationCategory\n    __typename\n  }\n}"


class SearchRelationCategoryQueryOptions(RelationCategoryTrait, BaseModel):
    typename: Literal["RelationCategory"] = Field(
        alias="__typename", default="RelationCategory", exclude=True
    )
    value: ID
    "The unique identifier of the expression within its graph"
    label: str
    "The unique identifier of the expression within its graph"
    model_config = ConfigDict(frozen=True)


class SearchRelationCategoryQuery(BaseModel):
    options: Tuple[SearchRelationCategoryQueryOptions, ...]
    "List of all relation categories"

    class Arguments(BaseModel):
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)

    class Meta:
        document = "query SearchRelationCategory($search: String, $values: [ID!]) {\n  options: relationCategories(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: 10}\n  ) {\n    value: id\n    label: label\n    __typename\n  }\n}"


class GetStructureCategoryQuery(BaseModel):
    structure_category: StructureCategory = Field(alias="structureCategory")

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment BaseCategory on Category {\n  id\n  label\n  ageName\n  __typename\n}\n\nfragment BaseNodeCategory on NodeCategory {\n  id\n  __typename\n}\n\nfragment StructureCategory on StructureCategory {\n  ...BaseCategory\n  ...BaseNodeCategory\n  identifier\n  __typename\n}\n\nquery GetStructureCategory($id: ID!) {\n  structureCategory(id: $id) {\n    ...StructureCategory\n    __typename\n  }\n}"


class SearchStructureCategoryQueryOptions(StructureCategoryTrait, BaseModel):
    typename: Literal["StructureCategory"] = Field(
        alias="__typename", default="StructureCategory", exclude=True
    )
    value: ID
    "The unique identifier of the expression within its graph"
    label: str
    "The unique identifier of the expression within its graph"
    model_config = ConfigDict(frozen=True)


class SearchStructureCategoryQuery(BaseModel):
    options: Tuple[SearchStructureCategoryQueryOptions, ...]
    "List of all structure categories"

    class Arguments(BaseModel):
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)

    class Meta:
        document = "query SearchStructureCategory($search: String, $values: [ID!]) {\n  options: structureCategories(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: 10}\n  ) {\n    value: id\n    label: label\n    __typename\n  }\n}"


class GetGenericCategoryQuery(BaseModel):
    generic_category: GenericCategory = Field(alias="genericCategory")

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment BaseCategory on Category {\n  id\n  label\n  ageName\n  __typename\n}\n\nfragment BaseNodeCategory on NodeCategory {\n  id\n  __typename\n}\n\nfragment GenericCategory on GenericCategory {\n  ...BaseCategory\n  ...BaseNodeCategory\n  instanceKind\n  __typename\n}\n\nquery GetGenericCategory($id: ID!) {\n  genericCategory(id: $id) {\n    ...GenericCategory\n    __typename\n  }\n}"


class SearchGenericCategoryQueryOptions(GenericCategoryTrait, BaseModel):
    typename: Literal["GenericCategory"] = Field(
        alias="__typename", default="GenericCategory", exclude=True
    )
    value: ID
    "The unique identifier of the expression within its graph"
    label: str
    "The unique identifier of the expression within its graph"
    model_config = ConfigDict(frozen=True)


class SearchGenericCategoryQuery(BaseModel):
    options: Tuple[SearchGenericCategoryQueryOptions, ...]
    "List of all generic categories"

    class Arguments(BaseModel):
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)

    class Meta:
        document = "query SearchGenericCategory($search: String, $values: [ID!]) {\n  options: genericCategories(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: 10}\n  ) {\n    value: id\n    label: label\n    __typename\n  }\n}"


class GetModelQuery(BaseModel):
    model: Model

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment MediaStore on MediaStore {\n  id\n  presignedUrl\n  key\n  __typename\n}\n\nfragment Model on Model {\n  id\n  name\n  store {\n    ...MediaStore\n    __typename\n  }\n  __typename\n}\n\nquery GetModel($id: ID!) {\n  model(id: $id) {\n    ...Model\n    __typename\n  }\n}"


class SearchModelsQueryOptions(BaseModel):
    """A model represents a trained machine learning model that can be used for analysis."""

    typename: Literal["Model"] = Field(
        alias="__typename", default="Model", exclude=True
    )
    value: ID
    "The unique identifier of the model"
    label: str
    "The name of the model"
    model_config = ConfigDict(frozen=True)


class SearchModelsQuery(BaseModel):
    options: Tuple[SearchModelsQueryOptions, ...]
    "List of all deep learning models (e.g. neural networks)"

    class Arguments(BaseModel):
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)

    class Meta:
        document = "query SearchModels($search: String, $values: [ID!]) {\n  options: models(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: 10}\n  ) {\n    value: id\n    label: name\n    __typename\n  }\n}"


class GetGraphQueryQuery(BaseModel):
    graph_query: GraphQuery = Field(alias="graphQuery")

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment ListScatterPlot on ScatterPlot {\n  id\n  name\n  xColumn\n  yColumn\n  __typename\n}\n\nfragment GraphQuery on GraphQuery {\n  id\n  name\n  scatterPlots {\n    ...ListScatterPlot\n    __typename\n  }\n  __typename\n}\n\nquery GetGraphQuery($id: ID!) {\n  graphQuery(id: $id) {\n    ...GraphQuery\n    __typename\n  }\n}"


class SearchGraphQueriesQueryOptions(BaseModel):
    """A view of a graph, that contains entities and relations."""

    typename: Literal["GraphQuery"] = Field(
        alias="__typename", default="GraphQuery", exclude=True
    )
    value: ID
    label: str
    model_config = ConfigDict(frozen=True)


class SearchGraphQueriesQuery(BaseModel):
    options: Tuple[SearchGraphQueriesQueryOptions, ...]
    "List of all graph queries"

    class Arguments(BaseModel):
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)

    class Meta:
        document = "query SearchGraphQueries($search: String, $values: [ID!]) {\n  options: graphQueries(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: 10}\n  ) {\n    value: id\n    label: name\n    __typename\n  }\n}"


class GetGraphQuery(BaseModel):
    graph: Graph

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment Graph on Graph {\n  id\n  name\n  ontology {\n    id\n    __typename\n  }\n  __typename\n}\n\nquery GetGraph($id: ID!) {\n  graph(id: $id) {\n    ...Graph\n    __typename\n  }\n}"


class SearchGraphsQueryOptions(GraphTrait, BaseModel):
    """A graph, that contains entities and relations."""

    typename: Literal["Graph"] = Field(
        alias="__typename", default="Graph", exclude=True
    )
    value: ID
    label: str
    model_config = ConfigDict(frozen=True)


class SearchGraphsQuery(BaseModel):
    options: Tuple[SearchGraphsQueryOptions, ...]
    "List of all knowledge graphs"

    class Arguments(BaseModel):
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)

    class Meta:
        document = "query SearchGraphs($search: String, $values: [ID!]) {\n  options: graphs(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: 10}\n  ) {\n    value: id\n    label: name\n    __typename\n  }\n}"


class GetProtocolStepQuery(BaseModel):
    protocol_step: ProtocolStep = Field(alias="protocolStep")

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment ProtocolStep on ProtocolStep {\n  id\n  template {\n    id\n    name\n    __typename\n  }\n  reagentMappings {\n    reagent {\n      id\n      __typename\n    }\n    __typename\n  }\n  forReagent {\n    id\n    __typename\n  }\n  __typename\n}\n\nquery GetProtocolStep($id: ID!) {\n  protocolStep(id: $id) {\n    ...ProtocolStep\n    __typename\n  }\n}"


class SearchProtocolStepsQueryOptions(BaseModel):
    typename: Literal["ProtocolStep"] = Field(
        alias="__typename", default="ProtocolStep", exclude=True
    )
    value: ID
    label: str
    model_config = ConfigDict(frozen=True)


class SearchProtocolStepsQuery(BaseModel):
    options: Tuple[SearchProtocolStepsQueryOptions, ...]
    "List of all protocol steps"

    class Arguments(BaseModel):
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)

    class Meta:
        document = "query SearchProtocolSteps($search: String, $values: [ID!]) {\n  options: protocolSteps(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: 10}\n  ) {\n    value: id\n    label: name\n    __typename\n  }\n}"


class GetPlotViewQuery(BaseModel):
    plot_view: PlotView = Field(alias="plotView")

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment BaseNode on Node {\n  id\n  label\n  __typename\n}\n\nfragment Entity on Entity {\n  id\n  category {\n    id\n    label\n    __typename\n  }\n  __typename\n}\n\nfragment BaseEdge on Edge {\n  id\n  leftId\n  rightId\n  __typename\n}\n\nfragment Relation on Relation {\n  category {\n    id\n    label\n    __typename\n  }\n  __typename\n}\n\nfragment Structure on Structure {\n  id\n  object\n  identifier\n  __typename\n}\n\nfragment Measurement on Measurement {\n  value\n  category {\n    id\n    label\n    metricKind\n    __typename\n  }\n  __typename\n}\n\nfragment Edge on Edge {\n  ...BaseEdge\n  ...Measurement\n  ...Relation\n  __typename\n}\n\nfragment Node on Node {\n  ...BaseNode\n  ...Entity\n  ...Structure\n  __typename\n}\n\nfragment Table on Table {\n  rows\n  columns {\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment Path on Path {\n  nodes {\n    ...Node\n    __typename\n  }\n  edges {\n    ...Edge\n    __typename\n  }\n  __typename\n}\n\nfragment Pairs on Pairs {\n  pairs {\n    left {\n      id\n      __typename\n    }\n    right {\n      id\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment GraphView on GraphView {\n  id\n  query {\n    id\n    name\n    __typename\n  }\n  render {\n    ...Path\n    ...Pairs\n    ...Table\n    __typename\n  }\n  __typename\n}\n\nfragment ScatterPlot on ScatterPlot {\n  id\n  name\n  __typename\n}\n\nfragment PlotView on PlotView {\n  view {\n    ...GraphView\n    __typename\n  }\n  plot {\n    ...ScatterPlot\n    __typename\n  }\n  __typename\n}\n\nquery GetPlotView($id: ID!) {\n  plotView(id: $id) {\n    ...PlotView\n    __typename\n  }\n}"


class SearchPlotViewsQueryOptions(BaseModel):
    """A view of a graph, that contains entities and relations."""

    typename: Literal["PlotView"] = Field(
        alias="__typename", default="PlotView", exclude=True
    )
    value: ID
    label: str
    model_config = ConfigDict(frozen=True)


class SearchPlotViewsQuery(BaseModel):
    options: Tuple[SearchPlotViewsQueryOptions, ...]
    "List of all plot views"

    class Arguments(BaseModel):
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)

    class Meta:
        document = "query SearchPlotViews($search: String, $values: [ID!]) {\n  options: plotViews(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: 10}\n  ) {\n    value: id\n    label: name\n    __typename\n  }\n}"


class GetNodeCategoryQueryNodecategoryBase(BaseModel):
    pass
    model_config = ConfigDict(frozen=True)


class GetNodeCategoryQueryNodecategoryBaseStructureCategory(
    NodeCategoryStructureCategory, GetNodeCategoryQueryNodecategoryBase, BaseModel
):
    typename: Literal["StructureCategory"] = Field(
        alias="__typename", default="StructureCategory", exclude=True
    )


class GetNodeCategoryQueryNodecategoryBaseGenericCategory(
    NodeCategoryGenericCategory, GetNodeCategoryQueryNodecategoryBase, BaseModel
):
    typename: Literal["GenericCategory"] = Field(
        alias="__typename", default="GenericCategory", exclude=True
    )


class GetNodeCategoryQuery(BaseModel):
    node_category: Annotated[
        Union[
            GetNodeCategoryQueryNodecategoryBaseStructureCategory,
            GetNodeCategoryQueryNodecategoryBaseGenericCategory,
        ],
        Field(discriminator="typename"),
    ] = Field(alias="nodeCategory")

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment BaseNodeCategory on NodeCategory {\n  id\n  __typename\n}\n\nfragment BaseCategory on Category {\n  id\n  label\n  ageName\n  __typename\n}\n\nfragment StructureCategory on StructureCategory {\n  ...BaseCategory\n  ...BaseNodeCategory\n  identifier\n  __typename\n}\n\nfragment GenericCategory on GenericCategory {\n  ...BaseCategory\n  ...BaseNodeCategory\n  instanceKind\n  __typename\n}\n\nfragment NodeCategory on NodeCategory {\n  ...StructureCategory\n  ...GenericCategory\n  __typename\n}\n\nquery GetNodeCategory($id: ID!) {\n  nodeCategory(id: $id) {\n    ...NodeCategory\n    __typename\n  }\n}"


class GetNodeViewQuery(BaseModel):
    node_view: NodeView = Field(alias="nodeView")

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment BaseNode on Node {\n  id\n  label\n  __typename\n}\n\nfragment Entity on Entity {\n  id\n  category {\n    id\n    label\n    __typename\n  }\n  __typename\n}\n\nfragment BaseEdge on Edge {\n  id\n  leftId\n  rightId\n  __typename\n}\n\nfragment Relation on Relation {\n  category {\n    id\n    label\n    __typename\n  }\n  __typename\n}\n\nfragment Structure on Structure {\n  id\n  object\n  identifier\n  __typename\n}\n\nfragment Measurement on Measurement {\n  value\n  category {\n    id\n    label\n    metricKind\n    __typename\n  }\n  __typename\n}\n\nfragment Edge on Edge {\n  ...BaseEdge\n  ...Measurement\n  ...Relation\n  __typename\n}\n\nfragment Node on Node {\n  ...BaseNode\n  ...Entity\n  ...Structure\n  __typename\n}\n\nfragment Pairs on Pairs {\n  pairs {\n    left {\n      id\n      __typename\n    }\n    right {\n      id\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment Table on Table {\n  rows\n  columns {\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment Path on Path {\n  nodes {\n    ...Node\n    __typename\n  }\n  edges {\n    ...Edge\n    __typename\n  }\n  __typename\n}\n\nfragment NodeView on NodeView {\n  id\n  query {\n    id\n    name\n    __typename\n  }\n  render {\n    ...Path\n    ...Pairs\n    ...Table\n    __typename\n  }\n  __typename\n}\n\nquery GetNodeView($id: ID!) {\n  nodeView(id: $id) {\n    ...NodeView\n    __typename\n  }\n}"


class SearchNodeViewsQueryOptions(BaseModel):
    """A view of a graph, that contains entities and relations."""

    typename: Literal["NodeView"] = Field(
        alias="__typename", default="NodeView", exclude=True
    )
    value: ID
    label: str
    model_config = ConfigDict(frozen=True)


class SearchNodeViewsQuery(BaseModel):
    options: Tuple[SearchNodeViewsQueryOptions, ...]
    "List of all node views"

    class Arguments(BaseModel):
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)

    class Meta:
        document = "query SearchNodeViews($search: String, $values: [ID!]) {\n  options: nodeViews(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: 10}\n  ) {\n    value: id\n    label: label\n    __typename\n  }\n}"


class GetMeasurmentCategoryQuery(BaseModel):
    measurement_category: MeasurementCategory = Field(alias="measurementCategory")

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment BaseCategory on Category {\n  id\n  label\n  ageName\n  __typename\n}\n\nfragment BaseEdgeCategory on EdgeCategory {\n  left {\n    id\n    __typename\n  }\n  right {\n    id\n    __typename\n  }\n  __typename\n}\n\nfragment MeasurementCategory on MeasurementCategory {\n  ...BaseCategory\n  ...BaseEdgeCategory\n  metricKind\n  __typename\n}\n\nquery GetMeasurmentCategory($id: ID!) {\n  measurementCategory(id: $id) {\n    ...MeasurementCategory\n    __typename\n  }\n}"


class SearchMeasurmentCategoryQueryOptions(MeasurementCategoryTrait, BaseModel):
    typename: Literal["MeasurementCategory"] = Field(
        alias="__typename", default="MeasurementCategory", exclude=True
    )
    value: ID
    "The unique identifier of the expression within its graph"
    label: str
    "The unique identifier of the expression within its graph"
    model_config = ConfigDict(frozen=True)


class SearchMeasurmentCategoryQuery(BaseModel):
    options: Tuple[SearchMeasurmentCategoryQueryOptions, ...]
    "List of all measurement categories"

    class Arguments(BaseModel):
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)

    class Meta:
        document = "query SearchMeasurmentCategory($search: String, $values: [ID!]) {\n  options: measurementCategories(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: 10}\n  ) {\n    value: id\n    label: label\n    __typename\n  }\n}"


class GetReagentQuery(BaseModel):
    reagent: Reagent

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment Reagent on Reagent {\n  id\n  expression {\n    id\n    __typename\n  }\n  lotId\n  __typename\n}\n\nquery GetReagent($id: ID!) {\n  reagent(id: $id) {\n    ...Reagent\n    __typename\n  }\n}"


class SearchReagentsQueryOptions(BaseModel):
    typename: Literal["Reagent"] = Field(
        alias="__typename", default="Reagent", exclude=True
    )
    value: ID
    label: str
    model_config = ConfigDict(frozen=True)


class SearchReagentsQuery(BaseModel):
    options: Tuple[SearchReagentsQueryOptions, ...]
    "List of all reagents used in protocols"

    class Arguments(BaseModel):
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)

    class Meta:
        document = "query SearchReagents($search: String, $values: [ID!]) {\n  options: reagents(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: 10}\n  ) {\n    value: id\n    label: label\n    __typename\n  }\n}"


class GetNodeQueryNodeBase(BaseModel):
    pass
    model_config = ConfigDict(frozen=True)


class GetNodeQueryNodeBaseEntity(NodeEntity, GetNodeQueryNodeBase, BaseModel):
    typename: Literal["Entity"] = Field(
        alias="__typename", default="Entity", exclude=True
    )


class GetNodeQueryNodeBaseStructure(NodeStructure, GetNodeQueryNodeBase, BaseModel):
    typename: Literal["Structure"] = Field(
        alias="__typename", default="Structure", exclude=True
    )


class GetNodeQuery(BaseModel):
    node: Annotated[
        Union[GetNodeQueryNodeBaseEntity, GetNodeQueryNodeBaseStructure],
        Field(discriminator="typename"),
    ]

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment BaseNode on Node {\n  id\n  label\n  __typename\n}\n\nfragment Structure on Structure {\n  id\n  object\n  identifier\n  __typename\n}\n\nfragment Entity on Entity {\n  id\n  category {\n    id\n    label\n    __typename\n  }\n  __typename\n}\n\nfragment Node on Node {\n  ...BaseNode\n  ...Entity\n  ...Structure\n  __typename\n}\n\nquery GetNode($id: ID!) {\n  node(id: $id) {\n    ...Node\n    __typename\n  }\n}"


class SearchEntitiesQueryOptions(EntityTrait, BaseModel):
    """A Entity is a recorded data point in a graph. It can measure a property of an entity through a direct measurement edge, that connects the entity to the structure. It of course can relate to other structures through relation edges."""

    typename: Literal["Entity"] = Field(
        alias="__typename", default="Entity", exclude=True
    )
    value: NodeID
    "The unique identifier of the entity within its graph"
    label: str
    model_config = ConfigDict(frozen=True)


class SearchEntitiesQuery(BaseModel):
    options: Tuple[SearchEntitiesQueryOptions, ...]
    "List of all entities in the system"

    class Arguments(BaseModel):
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)

    class Meta:
        document = "query SearchEntities($search: String, $values: [ID!]) {\n  options: nodes(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: 10}\n  ) {\n    value: id\n    label: label\n    __typename\n  }\n}"


class GetGraphViewQuery(BaseModel):
    graph_view: GraphView = Field(alias="graphView")

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment BaseNode on Node {\n  id\n  label\n  __typename\n}\n\nfragment Entity on Entity {\n  id\n  category {\n    id\n    label\n    __typename\n  }\n  __typename\n}\n\nfragment BaseEdge on Edge {\n  id\n  leftId\n  rightId\n  __typename\n}\n\nfragment Relation on Relation {\n  category {\n    id\n    label\n    __typename\n  }\n  __typename\n}\n\nfragment Structure on Structure {\n  id\n  object\n  identifier\n  __typename\n}\n\nfragment Measurement on Measurement {\n  value\n  category {\n    id\n    label\n    metricKind\n    __typename\n  }\n  __typename\n}\n\nfragment Edge on Edge {\n  ...BaseEdge\n  ...Measurement\n  ...Relation\n  __typename\n}\n\nfragment Node on Node {\n  ...BaseNode\n  ...Entity\n  ...Structure\n  __typename\n}\n\nfragment Pairs on Pairs {\n  pairs {\n    left {\n      id\n      __typename\n    }\n    right {\n      id\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment Table on Table {\n  rows\n  columns {\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment Path on Path {\n  nodes {\n    ...Node\n    __typename\n  }\n  edges {\n    ...Edge\n    __typename\n  }\n  __typename\n}\n\nfragment GraphView on GraphView {\n  id\n  query {\n    id\n    name\n    __typename\n  }\n  render {\n    ...Path\n    ...Pairs\n    ...Table\n    __typename\n  }\n  __typename\n}\n\nquery GetGraphView($id: ID!) {\n  graphView(id: $id) {\n    ...GraphView\n    __typename\n  }\n}"


class SearchGraphViewsQueryOptions(BaseModel):
    """A view of a graph, that contains entities and relations."""

    typename: Literal["GraphView"] = Field(
        alias="__typename", default="GraphView", exclude=True
    )
    value: ID
    label: str
    model_config = ConfigDict(frozen=True)


class SearchGraphViewsQuery(BaseModel):
    options: Tuple[SearchGraphViewsQueryOptions, ...]
    "List of all graph views"

    class Arguments(BaseModel):
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)

    class Meta:
        document = "query SearchGraphViews($search: String, $values: [ID!]) {\n  options: graphViews(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: 10}\n  ) {\n    value: id\n    label: label\n    __typename\n  }\n}"


class GetOntologyQuery(BaseModel):
    ontology: Ontology

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment BaseNodeCategory on NodeCategory {\n  id\n  __typename\n}\n\nfragment BaseListEdgeCategory on EdgeCategory {\n  left {\n    id\n    __typename\n  }\n  right {\n    id\n    __typename\n  }\n  __typename\n}\n\nfragment BaseListCategory on Category {\n  id\n  label\n  description\n  ageName\n  store {\n    presignedUrl\n    __typename\n  }\n  __typename\n}\n\nfragment BaseListNodeCategory on NodeCategory {\n  id\n  __typename\n}\n\nfragment ListGraphQuery on GraphQuery {\n  id\n  name\n  query\n  description\n  __typename\n}\n\nfragment ListGenericCategory on GenericCategory {\n  ...BaseListCategory\n  ...BaseNodeCategory\n  instanceKind\n  __typename\n}\n\nfragment ListMeasurementCategory on MeasurementCategory {\n  ...BaseListCategory\n  ...BaseListEdgeCategory\n  metricKind\n  __typename\n}\n\nfragment ListStructureCategory on StructureCategory {\n  ...BaseListCategory\n  ...BaseListNodeCategory\n  identifier\n  __typename\n}\n\nfragment ListRelationCategory on RelationCategory {\n  ...BaseListCategory\n  ...BaseListEdgeCategory\n  __typename\n}\n\nfragment Ontology on Ontology {\n  id\n  name\n  structureCategories {\n    ...ListStructureCategory\n    __typename\n  }\n  genericCategories {\n    ...ListGenericCategory\n    __typename\n  }\n  relationCategories {\n    ...ListRelationCategory\n    __typename\n  }\n  measurementCategories {\n    ...ListMeasurementCategory\n    __typename\n  }\n  graphQueries {\n    ...ListGraphQuery\n    __typename\n  }\n  __typename\n}\n\nquery GetOntology($id: ID!) {\n  ontology(id: $id) {\n    ...Ontology\n    __typename\n  }\n}"


class SearchOntologiesQueryOptions(OntologyTrait, BaseModel):
    """An ontology represents a formal naming and definition of types, properties, and
    interrelationships between entities in a specific domain. In kraph, ontologies provide the vocabulary
    and semantic structure for organizing data across graphs."""

    typename: Literal["Ontology"] = Field(
        alias="__typename", default="Ontology", exclude=True
    )
    value: ID
    "The unique identifier of the ontology"
    label: str
    "The name of the ontology"
    model_config = ConfigDict(frozen=True)


class SearchOntologiesQuery(BaseModel):
    options: Tuple[SearchOntologiesQueryOptions, ...]
    "List of all ontologies"

    class Arguments(BaseModel):
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)

    class Meta:
        document = "query SearchOntologies($search: String, $values: [ID!]) {\n  options: ontologies(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: 10}\n  ) {\n    value: id\n    label: name\n    __typename\n  }\n}"


async def acreate_model(
    name: str,
    model: RemoteUpload,
    view: Optional[ID] = None,
    rath: Optional[KraphRath] = None,
) -> Model:
    """CreateModel

    Create a new model

    Arguments:
        name: The name of the model
        model: The uploaded model file (e.g. .h5, .onnx, .pt)
        view: Optional view ID to associate with the model
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Model"""
    return (
        await aexecute(
            CreateModelMutation,
            {"input": {"name": name, "model": model, "view": view}},
            rath=rath,
        )
    ).create_model


def create_model(
    name: str,
    model: RemoteUpload,
    view: Optional[ID] = None,
    rath: Optional[KraphRath] = None,
) -> Model:
    """CreateModel

    Create a new model

    Arguments:
        name: The name of the model
        model: The uploaded model file (e.g. .h5, .onnx, .pt)
        view: Optional view ID to associate with the model
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Model"""
    return execute(
        CreateModelMutation,
        {"input": {"name": name, "model": model, "view": view}},
        rath=rath,
    ).create_model


async def acreate_graph_query(
    name: str,
    query: Cypher,
    kind: ViewKind,
    ontology: Optional[ID] = None,
    description: Optional[str] = None,
    columns: Optional[Iterable[ColumnInput]] = None,
    test_against: Optional[ID] = None,
    rath: Optional[KraphRath] = None,
) -> CreateGraphQueryMutationCreategraphquery:
    """CreateGraphQuery

    Create a new graph query

    Arguments:
        ontology: The ID of the ontology this expression belongs to. If not provided, uses default ontology
        name: The label/name of the expression
        query: The label/name of the expression
        description: A detailed description of the expression
        kind: The kind/type of this expression
        columns: The columns (if ViewKind is Table)
        test_against: The graph to test against
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        CreateGraphQueryMutationCreategraphquery"""
    return (
        await aexecute(
            CreateGraphQueryMutation,
            {
                "input": {
                    "ontology": ontology,
                    "name": name,
                    "query": query,
                    "description": description,
                    "kind": kind,
                    "columns": columns,
                    "testAgainst": test_against,
                }
            },
            rath=rath,
        )
    ).create_graph_query


def create_graph_query(
    name: str,
    query: Cypher,
    kind: ViewKind,
    ontology: Optional[ID] = None,
    description: Optional[str] = None,
    columns: Optional[Iterable[ColumnInput]] = None,
    test_against: Optional[ID] = None,
    rath: Optional[KraphRath] = None,
) -> CreateGraphQueryMutationCreategraphquery:
    """CreateGraphQuery

    Create a new graph query

    Arguments:
        ontology: The ID of the ontology this expression belongs to. If not provided, uses default ontology
        name: The label/name of the expression
        query: The label/name of the expression
        description: A detailed description of the expression
        kind: The kind/type of this expression
        columns: The columns (if ViewKind is Table)
        test_against: The graph to test against
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        CreateGraphQueryMutationCreategraphquery"""
    return execute(
        CreateGraphQueryMutation,
        {
            "input": {
                "ontology": ontology,
                "name": name,
                "query": query,
                "description": description,
                "kind": kind,
                "columns": columns,
                "testAgainst": test_against,
            }
        },
        rath=rath,
    ).create_graph_query


async def acreate_plot_view(
    plot: ID, view: ID, rath: Optional[KraphRath] = None
) -> PlotView:
    """CreatePlotView

    Create a new plot view

    Arguments:
        plot: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
        view: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        PlotView"""
    return (
        await aexecute(
            CreatePlotViewMutation, {"input": {"plot": plot, "view": view}}, rath=rath
        )
    ).create_plot_view


def create_plot_view(plot: ID, view: ID, rath: Optional[KraphRath] = None) -> PlotView:
    """CreatePlotView

    Create a new plot view

    Arguments:
        plot: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
        view: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        PlotView"""
    return execute(
        CreatePlotViewMutation, {"input": {"plot": plot, "view": view}}, rath=rath
    ).create_plot_view


async def acreate_graph(
    name: str,
    ontology: Optional[ID] = None,
    experiment: Optional[ID] = None,
    description: Optional[str] = None,
    rath: Optional[KraphRath] = None,
) -> Graph:
    """CreateGraph

    Create a new graph

    Arguments:
        name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
        ontology: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID.
        experiment: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID.
        description: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Graph"""
    return (
        await aexecute(
            CreateGraphMutation,
            {
                "input": {
                    "name": name,
                    "ontology": ontology,
                    "experiment": experiment,
                    "description": description,
                }
            },
            rath=rath,
        )
    ).create_graph


def create_graph(
    name: str,
    ontology: Optional[ID] = None,
    experiment: Optional[ID] = None,
    description: Optional[str] = None,
    rath: Optional[KraphRath] = None,
) -> Graph:
    """CreateGraph

    Create a new graph

    Arguments:
        name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
        ontology: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID.
        experiment: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID.
        description: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Graph"""
    return execute(
        CreateGraphMutation,
        {
            "input": {
                "name": name,
                "ontology": ontology,
                "experiment": experiment,
                "description": description,
            }
        },
        rath=rath,
    ).create_graph


async def arequest_upload(
    key: str, datalayer: str, rath: Optional[KraphRath] = None
) -> PresignedPostCredentials:
    """RequestUpload

    Request a new file upload

    Arguments:
        key: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
        datalayer: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        PresignedPostCredentials"""
    return (
        await aexecute(
            RequestUploadMutation,
            {"input": {"key": key, "datalayer": datalayer}},
            rath=rath,
        )
    ).request_upload


def request_upload(
    key: str, datalayer: str, rath: Optional[KraphRath] = None
) -> PresignedPostCredentials:
    """RequestUpload

    Request a new file upload

    Arguments:
        key: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
        datalayer: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        PresignedPostCredentials"""
    return execute(
        RequestUploadMutation,
        {"input": {"key": key, "datalayer": datalayer}},
        rath=rath,
    ).request_upload


async def acreate_protocol_step(
    template: ID,
    entity: ID,
    reagent_mappings: Iterable[ReagentMappingInput],
    value_mappings: Iterable[VariableInput],
    performed_at: Optional[datetime] = None,
    performed_by: Optional[ID] = None,
    rath: Optional[KraphRath] = None,
) -> ProtocolStep:
    """CreateProtocolStep

    Create a new protocol step

    Arguments:
        template: ID of the protocol step template
        entity: ID of the entity this step is performed on
        reagent_mappings: List of reagent mappings
        value_mappings: List of variable mappings
        performed_at: When the step was performed
        performed_by: ID of the user who performed the step
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        ProtocolStep"""
    return (
        await aexecute(
            CreateProtocolStepMutation,
            {
                "input": {
                    "template": template,
                    "entity": entity,
                    "reagentMappings": reagent_mappings,
                    "valueMappings": value_mappings,
                    "performedAt": performed_at,
                    "performedBy": performed_by,
                }
            },
            rath=rath,
        )
    ).create_protocol_step


def create_protocol_step(
    template: ID,
    entity: ID,
    reagent_mappings: Iterable[ReagentMappingInput],
    value_mappings: Iterable[VariableInput],
    performed_at: Optional[datetime] = None,
    performed_by: Optional[ID] = None,
    rath: Optional[KraphRath] = None,
) -> ProtocolStep:
    """CreateProtocolStep

    Create a new protocol step

    Arguments:
        template: ID of the protocol step template
        entity: ID of the entity this step is performed on
        reagent_mappings: List of reagent mappings
        value_mappings: List of variable mappings
        performed_at: When the step was performed
        performed_by: ID of the user who performed the step
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        ProtocolStep"""
    return execute(
        CreateProtocolStepMutation,
        {
            "input": {
                "template": template,
                "entity": entity,
                "reagentMappings": reagent_mappings,
                "valueMappings": value_mappings,
                "performedAt": performed_at,
                "performedBy": performed_by,
            }
        },
        rath=rath,
    ).create_protocol_step


async def acreate_scatter_plot(
    query: ID,
    name: str,
    id_column: str,
    x_column: str,
    y_column: str,
    description: Optional[str] = None,
    x_id_column: Optional[str] = None,
    y_id_column: Optional[str] = None,
    size_column: Optional[str] = None,
    color_column: Optional[str] = None,
    shape_column: Optional[str] = None,
    test_against: Optional[ID] = None,
    rath: Optional[KraphRath] = None,
) -> ScatterPlot:
    """CreateScatterPlot

    Create a new scatter plot

    Arguments:
        query: The query to use
        name: The label/name of the expression
        description: A detailed description of the expression
        id_column: The column to use for the ID of the points
        x_column: The column to use for the x-axis
        x_id_column: The column to use for the x-axis ID (node, or edge)
        y_column: The column to use for the y-axis
        y_id_column: The column to use for the y-axis ID (node, or edge)
        size_column: The column to use for the size of the points
        color_column: The column to use for the color of the points
        shape_column: The column to use for the shape of the points
        test_against: The graph to test against
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        ScatterPlot"""
    return (
        await aexecute(
            CreateScatterPlotMutation,
            {
                "input": {
                    "query": query,
                    "name": name,
                    "description": description,
                    "idColumn": id_column,
                    "xColumn": x_column,
                    "xIdColumn": x_id_column,
                    "yColumn": y_column,
                    "yIdColumn": y_id_column,
                    "sizeColumn": size_column,
                    "colorColumn": color_column,
                    "shapeColumn": shape_column,
                    "testAgainst": test_against,
                }
            },
            rath=rath,
        )
    ).create_scatter_plot


def create_scatter_plot(
    query: ID,
    name: str,
    id_column: str,
    x_column: str,
    y_column: str,
    description: Optional[str] = None,
    x_id_column: Optional[str] = None,
    y_id_column: Optional[str] = None,
    size_column: Optional[str] = None,
    color_column: Optional[str] = None,
    shape_column: Optional[str] = None,
    test_against: Optional[ID] = None,
    rath: Optional[KraphRath] = None,
) -> ScatterPlot:
    """CreateScatterPlot

    Create a new scatter plot

    Arguments:
        query: The query to use
        name: The label/name of the expression
        description: A detailed description of the expression
        id_column: The column to use for the ID of the points
        x_column: The column to use for the x-axis
        x_id_column: The column to use for the x-axis ID (node, or edge)
        y_column: The column to use for the y-axis
        y_id_column: The column to use for the y-axis ID (node, or edge)
        size_column: The column to use for the size of the points
        color_column: The column to use for the color of the points
        shape_column: The column to use for the shape of the points
        test_against: The graph to test against
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        ScatterPlot"""
    return execute(
        CreateScatterPlotMutation,
        {
            "input": {
                "query": query,
                "name": name,
                "description": description,
                "idColumn": id_column,
                "xColumn": x_column,
                "xIdColumn": x_id_column,
                "yColumn": y_column,
                "yIdColumn": y_id_column,
                "sizeColumn": size_column,
                "colorColumn": color_column,
                "shapeColumn": shape_column,
                "testAgainst": test_against,
            }
        },
        rath=rath,
    ).create_scatter_plot


async def acreate_node_view(
    query: ID, node: ID, rath: Optional[KraphRath] = None
) -> NodeView:
    """CreateNodeView

    Create a new node view

    Arguments:
        query: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
        node: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        NodeView"""
    return (
        await aexecute(
            CreateNodeViewMutation, {"input": {"query": query, "node": node}}, rath=rath
        )
    ).create_node_view


def create_node_view(query: ID, node: ID, rath: Optional[KraphRath] = None) -> NodeView:
    """CreateNodeView

    Create a new node view

    Arguments:
        query: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
        node: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        NodeView"""
    return execute(
        CreateNodeViewMutation, {"input": {"query": query, "node": node}}, rath=rath
    ).create_node_view


async def acreate_node_query(
    name: str,
    query: Cypher,
    kind: ViewKind,
    ontology: Optional[ID] = None,
    description: Optional[str] = None,
    columns: Optional[Iterable[ColumnInput]] = None,
    test_against: Optional[ID] = None,
    allowed_entities: Optional[Iterable[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> CreateNodeQueryMutationCreatenodequery:
    """CreateNodeQuery

    Create a new node query

    Arguments:
        ontology: The ID of the ontology this expression belongs to. If not provided, uses default ontology
        name: The label/name of the expression
        query: The label/name of the expression
        description: A detailed description of the expression
        kind: The kind/type of this expression
        columns: The columns (if ViewKind is Table)
        test_against: The node to test against
        allowed_entities: The allowed entitie classes for this query
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        CreateNodeQueryMutationCreatenodequery"""
    return (
        await aexecute(
            CreateNodeQueryMutation,
            {
                "input": {
                    "ontology": ontology,
                    "name": name,
                    "query": query,
                    "description": description,
                    "kind": kind,
                    "columns": columns,
                    "testAgainst": test_against,
                    "allowedEntities": allowed_entities,
                }
            },
            rath=rath,
        )
    ).create_node_query


def create_node_query(
    name: str,
    query: Cypher,
    kind: ViewKind,
    ontology: Optional[ID] = None,
    description: Optional[str] = None,
    columns: Optional[Iterable[ColumnInput]] = None,
    test_against: Optional[ID] = None,
    allowed_entities: Optional[Iterable[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> CreateNodeQueryMutationCreatenodequery:
    """CreateNodeQuery

    Create a new node query

    Arguments:
        ontology: The ID of the ontology this expression belongs to. If not provided, uses default ontology
        name: The label/name of the expression
        query: The label/name of the expression
        description: A detailed description of the expression
        kind: The kind/type of this expression
        columns: The columns (if ViewKind is Table)
        test_against: The node to test against
        allowed_entities: The allowed entitie classes for this query
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        CreateNodeQueryMutationCreatenodequery"""
    return execute(
        CreateNodeQueryMutation,
        {
            "input": {
                "ontology": ontology,
                "name": name,
                "query": query,
                "description": description,
                "kind": kind,
                "columns": columns,
                "testAgainst": test_against,
                "allowedEntities": allowed_entities,
            }
        },
        rath=rath,
    ).create_node_query


async def acreate_relation(
    left: ID, right: ID, kind: ID, rath: Optional[KraphRath] = None
) -> Relation:
    """CreateRelation

    Create a new relation between entities

    Arguments:
        left: ID of the left entity (format: graph:id)
        right: ID of the right entity (format: graph:id)
        kind: ID of the relation kind (LinkedExpression)
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Relation"""
    return (
        await aexecute(
            CreateRelationMutation,
            {"input": {"left": left, "right": right, "kind": kind}},
            rath=rath,
        )
    ).create_relation


def create_relation(
    left: ID, right: ID, kind: ID, rath: Optional[KraphRath] = None
) -> Relation:
    """CreateRelation

    Create a new relation between entities

    Arguments:
        left: ID of the left entity (format: graph:id)
        right: ID of the right entity (format: graph:id)
        kind: ID of the relation kind (LinkedExpression)
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Relation"""
    return execute(
        CreateRelationMutation,
        {"input": {"left": left, "right": right, "kind": kind}},
        rath=rath,
    ).create_relation


async def acreate_reagent(
    lot_id: str, expression: ID, rath: Optional[KraphRath] = None
) -> Reagent:
    """CreateReagent

    Create a new reagent

    Arguments:
        lot_id: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
        expression: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Reagent"""
    return (
        await aexecute(
            CreateReagentMutation,
            {"input": {"lotId": lot_id, "expression": expression}},
            rath=rath,
        )
    ).create_reagent


def create_reagent(
    lot_id: str, expression: ID, rath: Optional[KraphRath] = None
) -> Reagent:
    """CreateReagent

    Create a new reagent

    Arguments:
        lot_id: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
        expression: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Reagent"""
    return execute(
        CreateReagentMutation,
        {"input": {"lotId": lot_id, "expression": expression}},
        rath=rath,
    ).create_reagent


async def acreate_entity(
    graph: ID,
    expression: ID,
    name: Optional[str] = None,
    rath: Optional[KraphRath] = None,
) -> Entity:
    """CreateEntity

    Create a new entity

    Arguments:
        graph: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
        expression: The ID of the kind (LinkedExpression) to create the entity from
        name: Optional name for the entity
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Entity"""
    return (
        await aexecute(
            CreateEntityMutation,
            {"input": {"graph": graph, "expression": expression, "name": name}},
            rath=rath,
        )
    ).create_entity


def create_entity(
    graph: ID,
    expression: ID,
    name: Optional[str] = None,
    rath: Optional[KraphRath] = None,
) -> Entity:
    """CreateEntity

    Create a new entity

    Arguments:
        graph: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
        expression: The ID of the kind (LinkedExpression) to create the entity from
        name: Optional name for the entity
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Entity"""
    return execute(
        CreateEntityMutation,
        {"input": {"graph": graph, "expression": expression, "name": name}},
        rath=rath,
    ).create_entity


async def acreate_structure(
    structure: StructureString,
    graph: Optional[ID] = None,
    rath: Optional[KraphRath] = None,
) -> Structure:
    """CreateStructure

    Create a new structure

    Arguments:
        structure: The `StructureString` scalar type represents a string with a structure (required)
        graph: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Structure"""
    return (
        await aexecute(
            CreateStructureMutation,
            {"input": {"structure": structure, "graph": graph}},
            rath=rath,
        )
    ).create_structure


def create_structure(
    structure: StructureString,
    graph: Optional[ID] = None,
    rath: Optional[KraphRath] = None,
) -> Structure:
    """CreateStructure

    Create a new structure

    Arguments:
        structure: The `StructureString` scalar type represents a string with a structure (required)
        graph: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Structure"""
    return execute(
        CreateStructureMutation,
        {"input": {"structure": structure, "graph": graph}},
        rath=rath,
    ).create_structure


async def acreate_graph_view(
    query: ID, graph: ID, rath: Optional[KraphRath] = None
) -> GraphView:
    """CreateGraphView

    Create a new graph view

    Arguments:
        query: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
        graph: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        GraphView"""
    return (
        await aexecute(
            CreateGraphViewMutation,
            {"input": {"query": query, "graph": graph}},
            rath=rath,
        )
    ).create_graph_view


def create_graph_view(
    query: ID, graph: ID, rath: Optional[KraphRath] = None
) -> GraphView:
    """CreateGraphView

    Create a new graph view

    Arguments:
        query: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
        graph: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        GraphView"""
    return execute(
        CreateGraphViewMutation, {"input": {"query": query, "graph": graph}}, rath=rath
    ).create_graph_view


async def acreate_measurement_category(
    label: str,
    kind: MeasurementKind,
    ontology: Optional[ID] = None,
    description: Optional[str] = None,
    purl: Optional[str] = None,
    color: Optional[Iterable[int]] = None,
    image: Optional[RemoteUpload] = None,
    rath: Optional[KraphRath] = None,
) -> MeasurementCategory:
    """CreateMeasurementCategory

    Create a new expression

    Arguments:
        label: The label/name of the expression
        kind: The type of metric data this expression represents
        ontology: The ID of the ontology this expression belongs to. If not provided, uses default ontology
        description: A detailed description of the expression
        purl: Permanent URL identifier for the expression
        color: RGBA color values as list of 3 or 4 integers
        image: An optional image associated with this expression
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        MeasurementCategory"""
    return (
        await aexecute(
            CreateMeasurementCategoryMutation,
            {
                "input": {
                    "label": label,
                    "kind": kind,
                    "ontology": ontology,
                    "description": description,
                    "purl": purl,
                    "color": color,
                    "image": image,
                }
            },
            rath=rath,
        )
    ).create_measurement_category


def create_measurement_category(
    label: str,
    kind: MeasurementKind,
    ontology: Optional[ID] = None,
    description: Optional[str] = None,
    purl: Optional[str] = None,
    color: Optional[Iterable[int]] = None,
    image: Optional[RemoteUpload] = None,
    rath: Optional[KraphRath] = None,
) -> MeasurementCategory:
    """CreateMeasurementCategory

    Create a new expression

    Arguments:
        label: The label/name of the expression
        kind: The type of metric data this expression represents
        ontology: The ID of the ontology this expression belongs to. If not provided, uses default ontology
        description: A detailed description of the expression
        purl: Permanent URL identifier for the expression
        color: RGBA color values as list of 3 or 4 integers
        image: An optional image associated with this expression
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        MeasurementCategory"""
    return execute(
        CreateMeasurementCategoryMutation,
        {
            "input": {
                "label": label,
                "kind": kind,
                "ontology": ontology,
                "description": description,
                "purl": purl,
                "color": color,
                "image": image,
            }
        },
        rath=rath,
    ).create_measurement_category


async def acreate_structure_category(
    identifier: StructureIdentifier,
    ontology: Optional[ID] = None,
    description: Optional[str] = None,
    purl: Optional[str] = None,
    color: Optional[Iterable[int]] = None,
    image: Optional[RemoteUpload] = None,
    rath: Optional[KraphRath] = None,
) -> StructureCategory:
    """CreateStructureCategory

    Create a new expression

    Arguments:
        ontology: The ID of the ontology this expression belongs to. If not provided, uses default ontology
        identifier: The label/name of the expression
        description: A detailed description of the expression
        purl: Permanent URL identifier for the expression
        color: RGBA color values as list of 3 or 4 integers
        image: An optional image associated with this expression
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        StructureCategory"""
    return (
        await aexecute(
            CreateStructureCategoryMutation,
            {
                "input": {
                    "ontology": ontology,
                    "identifier": identifier,
                    "description": description,
                    "purl": purl,
                    "color": color,
                    "image": image,
                }
            },
            rath=rath,
        )
    ).create_structure_category


def create_structure_category(
    identifier: StructureIdentifier,
    ontology: Optional[ID] = None,
    description: Optional[str] = None,
    purl: Optional[str] = None,
    color: Optional[Iterable[int]] = None,
    image: Optional[RemoteUpload] = None,
    rath: Optional[KraphRath] = None,
) -> StructureCategory:
    """CreateStructureCategory

    Create a new expression

    Arguments:
        ontology: The ID of the ontology this expression belongs to. If not provided, uses default ontology
        identifier: The label/name of the expression
        description: A detailed description of the expression
        purl: Permanent URL identifier for the expression
        color: RGBA color values as list of 3 or 4 integers
        image: An optional image associated with this expression
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        StructureCategory"""
    return execute(
        CreateStructureCategoryMutation,
        {
            "input": {
                "ontology": ontology,
                "identifier": identifier,
                "description": description,
                "purl": purl,
                "color": color,
                "image": image,
            }
        },
        rath=rath,
    ).create_structure_category


async def acreate_generic_category(
    label: str,
    ontology: Optional[ID] = None,
    description: Optional[str] = None,
    purl: Optional[str] = None,
    color: Optional[Iterable[int]] = None,
    image: Optional[RemoteUpload] = None,
    rath: Optional[KraphRath] = None,
) -> GenericCategory:
    """CreateGenericCategory

    Create a new expression

    Arguments:
        ontology: The ID of the ontology this expression belongs to. If not provided, uses default ontology
        label: The label/name of the expression
        description: A detailed description of the expression
        purl: Permanent URL identifier for the expression
        color: RGBA color values as list of 3 or 4 integers
        image: An optional image associated with this expression
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        GenericCategory"""
    return (
        await aexecute(
            CreateGenericCategoryMutation,
            {
                "input": {
                    "ontology": ontology,
                    "label": label,
                    "description": description,
                    "purl": purl,
                    "color": color,
                    "image": image,
                }
            },
            rath=rath,
        )
    ).create_generic_category


def create_generic_category(
    label: str,
    ontology: Optional[ID] = None,
    description: Optional[str] = None,
    purl: Optional[str] = None,
    color: Optional[Iterable[int]] = None,
    image: Optional[RemoteUpload] = None,
    rath: Optional[KraphRath] = None,
) -> GenericCategory:
    """CreateGenericCategory

    Create a new expression

    Arguments:
        ontology: The ID of the ontology this expression belongs to. If not provided, uses default ontology
        label: The label/name of the expression
        description: A detailed description of the expression
        purl: Permanent URL identifier for the expression
        color: RGBA color values as list of 3 or 4 integers
        image: An optional image associated with this expression
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        GenericCategory"""
    return execute(
        CreateGenericCategoryMutation,
        {
            "input": {
                "ontology": ontology,
                "label": label,
                "description": description,
                "purl": purl,
                "color": color,
                "image": image,
            }
        },
        rath=rath,
    ).create_generic_category


async def acreate_relation_category(
    label: str,
    ontology: Optional[ID] = None,
    description: Optional[str] = None,
    purl: Optional[str] = None,
    color: Optional[Iterable[int]] = None,
    image: Optional[RemoteUpload] = None,
    rath: Optional[KraphRath] = None,
) -> RelationCategory:
    """CreateRelationCategory

    Create a new expression

    Arguments:
        ontology: The ID of the ontology this expression belongs to. If not provided, uses default ontology
        label: The label/name of the expression
        description: A detailed description of the expression
        purl: Permanent URL identifier for the expression
        color: RGBA color values as list of 3 or 4 integers
        image: An optional image associated with this expression
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        RelationCategory"""
    return (
        await aexecute(
            CreateRelationCategoryMutation,
            {
                "input": {
                    "ontology": ontology,
                    "label": label,
                    "description": description,
                    "purl": purl,
                    "color": color,
                    "image": image,
                }
            },
            rath=rath,
        )
    ).create_relation_category


def create_relation_category(
    label: str,
    ontology: Optional[ID] = None,
    description: Optional[str] = None,
    purl: Optional[str] = None,
    color: Optional[Iterable[int]] = None,
    image: Optional[RemoteUpload] = None,
    rath: Optional[KraphRath] = None,
) -> RelationCategory:
    """CreateRelationCategory

    Create a new expression

    Arguments:
        ontology: The ID of the ontology this expression belongs to. If not provided, uses default ontology
        label: The label/name of the expression
        description: A detailed description of the expression
        purl: Permanent URL identifier for the expression
        color: RGBA color values as list of 3 or 4 integers
        image: An optional image associated with this expression
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        RelationCategory"""
    return execute(
        CreateRelationCategoryMutation,
        {
            "input": {
                "ontology": ontology,
                "label": label,
                "description": description,
                "purl": purl,
                "color": color,
                "image": image,
            }
        },
        rath=rath,
    ).create_relation_category


async def acreate_measurement(
    structure: NodeID,
    entity: NodeID,
    expression: ID,
    value: Optional[Any] = None,
    valid_from: Optional[datetime] = None,
    valid_to: Optional[datetime] = None,
    rath: Optional[KraphRath] = None,
) -> Measurement:
    """CreateMeasurement

    Create a new metric for an entity

    Arguments:
        structure: The `NodeID` scalar type represents a graph node ID (required)
        entity: The `NodeID` scalar type represents a graph node ID (required)
        expression: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
        value: The `Metric` scalar type represents a matrix values as specified by
        valid_from: Date with time (isoformat)
        valid_to: Date with time (isoformat)
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Measurement"""
    return (
        await aexecute(
            CreateMeasurementMutation,
            {
                "input": {
                    "structure": structure,
                    "entity": entity,
                    "expression": expression,
                    "value": value,
                    "validFrom": valid_from,
                    "validTo": valid_to,
                }
            },
            rath=rath,
        )
    ).create_measurement


def create_measurement(
    structure: NodeID,
    entity: NodeID,
    expression: ID,
    value: Optional[Any] = None,
    valid_from: Optional[datetime] = None,
    valid_to: Optional[datetime] = None,
    rath: Optional[KraphRath] = None,
) -> Measurement:
    """CreateMeasurement

    Create a new metric for an entity

    Arguments:
        structure: The `NodeID` scalar type represents a graph node ID (required)
        entity: The `NodeID` scalar type represents a graph node ID (required)
        expression: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
        value: The `Metric` scalar type represents a matrix values as specified by
        valid_from: Date with time (isoformat)
        valid_to: Date with time (isoformat)
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Measurement"""
    return execute(
        CreateMeasurementMutation,
        {
            "input": {
                "structure": structure,
                "entity": entity,
                "expression": expression,
                "value": value,
                "validFrom": valid_from,
                "validTo": valid_to,
            }
        },
        rath=rath,
    ).create_measurement


async def acreate_ontology(
    name: str,
    description: Optional[str] = None,
    purl: Optional[str] = None,
    image: Optional[ID] = None,
    rath: Optional[KraphRath] = None,
) -> Ontology:
    """CreateOntology

    Create a new ontology

    Arguments:
        name: The name of the ontology (will be converted to snake_case)
        description: An optional description of the ontology
        purl: An optional PURL (Persistent URL) for the ontology
        image: An optional ID reference to an associated image
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Ontology"""
    return (
        await aexecute(
            CreateOntologyMutation,
            {
                "input": {
                    "name": name,
                    "description": description,
                    "purl": purl,
                    "image": image,
                }
            },
            rath=rath,
        )
    ).create_ontology


def create_ontology(
    name: str,
    description: Optional[str] = None,
    purl: Optional[str] = None,
    image: Optional[ID] = None,
    rath: Optional[KraphRath] = None,
) -> Ontology:
    """CreateOntology

    Create a new ontology

    Arguments:
        name: The name of the ontology (will be converted to snake_case)
        description: An optional description of the ontology
        purl: An optional PURL (Persistent URL) for the ontology
        image: An optional ID reference to an associated image
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Ontology"""
    return execute(
        CreateOntologyMutation,
        {
            "input": {
                "name": name,
                "description": description,
                "purl": purl,
                "image": image,
            }
        },
        rath=rath,
    ).create_ontology


async def aget_relation_category(
    id: ID, rath: Optional[KraphRath] = None
) -> RelationCategory:
    """GetRelationCategory


    Arguments:
        id (ID): No description
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        RelationCategory"""
    return (
        await aexecute(GetRelationCategoryQuery, {"id": id}, rath=rath)
    ).relation_category


def get_relation_category(id: ID, rath: Optional[KraphRath] = None) -> RelationCategory:
    """GetRelationCategory


    Arguments:
        id (ID): No description
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        RelationCategory"""
    return execute(GetRelationCategoryQuery, {"id": id}, rath=rath).relation_category


async def asearch_relation_category(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> Tuple[SearchRelationCategoryQueryOptions, ...]:
    """SearchRelationCategory

    List of all relation categories

    Arguments:
        search (Optional[str], optional): No description.
        values (Optional[List[ID]], optional): No description.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchRelationCategoryQueryRelationcategories]"""
    return (
        await aexecute(
            SearchRelationCategoryQuery, {"search": search, "values": values}, rath=rath
        )
    ).options


def search_relation_category(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> Tuple[SearchRelationCategoryQueryOptions, ...]:
    """SearchRelationCategory

    List of all relation categories

    Arguments:
        search (Optional[str], optional): No description.
        values (Optional[List[ID]], optional): No description.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchRelationCategoryQueryRelationcategories]"""
    return execute(
        SearchRelationCategoryQuery, {"search": search, "values": values}, rath=rath
    ).options


async def aget_structure_category(
    id: ID, rath: Optional[KraphRath] = None
) -> StructureCategory:
    """GetStructureCategory


    Arguments:
        id (ID): No description
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        StructureCategory"""
    return (
        await aexecute(GetStructureCategoryQuery, {"id": id}, rath=rath)
    ).structure_category


def get_structure_category(
    id: ID, rath: Optional[KraphRath] = None
) -> StructureCategory:
    """GetStructureCategory


    Arguments:
        id (ID): No description
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        StructureCategory"""
    return execute(GetStructureCategoryQuery, {"id": id}, rath=rath).structure_category


async def asearch_structure_category(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> Tuple[SearchStructureCategoryQueryOptions, ...]:
    """SearchStructureCategory

    List of all structure categories

    Arguments:
        search (Optional[str], optional): No description.
        values (Optional[List[ID]], optional): No description.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchStructureCategoryQueryStructurecategories]"""
    return (
        await aexecute(
            SearchStructureCategoryQuery,
            {"search": search, "values": values},
            rath=rath,
        )
    ).options


def search_structure_category(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> Tuple[SearchStructureCategoryQueryOptions, ...]:
    """SearchStructureCategory

    List of all structure categories

    Arguments:
        search (Optional[str], optional): No description.
        values (Optional[List[ID]], optional): No description.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchStructureCategoryQueryStructurecategories]"""
    return execute(
        SearchStructureCategoryQuery, {"search": search, "values": values}, rath=rath
    ).options


async def aget_generic_category(
    id: ID, rath: Optional[KraphRath] = None
) -> GenericCategory:
    """GetGenericCategory


    Arguments:
        id (ID): No description
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        GenericCategory"""
    return (
        await aexecute(GetGenericCategoryQuery, {"id": id}, rath=rath)
    ).generic_category


def get_generic_category(id: ID, rath: Optional[KraphRath] = None) -> GenericCategory:
    """GetGenericCategory


    Arguments:
        id (ID): No description
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        GenericCategory"""
    return execute(GetGenericCategoryQuery, {"id": id}, rath=rath).generic_category


async def asearch_generic_category(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> Tuple[SearchGenericCategoryQueryOptions, ...]:
    """SearchGenericCategory

    List of all generic categories

    Arguments:
        search (Optional[str], optional): No description.
        values (Optional[List[ID]], optional): No description.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchGenericCategoryQueryGenericcategories]"""
    return (
        await aexecute(
            SearchGenericCategoryQuery, {"search": search, "values": values}, rath=rath
        )
    ).options


def search_generic_category(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> Tuple[SearchGenericCategoryQueryOptions, ...]:
    """SearchGenericCategory

    List of all generic categories

    Arguments:
        search (Optional[str], optional): No description.
        values (Optional[List[ID]], optional): No description.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchGenericCategoryQueryGenericcategories]"""
    return execute(
        SearchGenericCategoryQuery, {"search": search, "values": values}, rath=rath
    ).options


async def aget_model(id: ID, rath: Optional[KraphRath] = None) -> Model:
    """GetModel


    Arguments:
        id (ID): No description
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Model"""
    return (await aexecute(GetModelQuery, {"id": id}, rath=rath)).model


def get_model(id: ID, rath: Optional[KraphRath] = None) -> Model:
    """GetModel


    Arguments:
        id (ID): No description
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Model"""
    return execute(GetModelQuery, {"id": id}, rath=rath).model


async def asearch_models(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> Tuple[SearchModelsQueryOptions, ...]:
    """SearchModels

    List of all deep learning models (e.g. neural networks)

    Arguments:
        search (Optional[str], optional): No description.
        values (Optional[List[ID]], optional): No description.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchModelsQueryModels]"""
    return (
        await aexecute(
            SearchModelsQuery, {"search": search, "values": values}, rath=rath
        )
    ).options


def search_models(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> Tuple[SearchModelsQueryOptions, ...]:
    """SearchModels

    List of all deep learning models (e.g. neural networks)

    Arguments:
        search (Optional[str], optional): No description.
        values (Optional[List[ID]], optional): No description.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchModelsQueryModels]"""
    return execute(
        SearchModelsQuery, {"search": search, "values": values}, rath=rath
    ).options


async def aget_graph_query(id: ID, rath: Optional[KraphRath] = None) -> GraphQuery:
    """GetGraphQuery


    Arguments:
        id (ID): No description
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        GraphQuery"""
    return (await aexecute(GetGraphQueryQuery, {"id": id}, rath=rath)).graph_query


def get_graph_query(id: ID, rath: Optional[KraphRath] = None) -> GraphQuery:
    """GetGraphQuery


    Arguments:
        id (ID): No description
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        GraphQuery"""
    return execute(GetGraphQueryQuery, {"id": id}, rath=rath).graph_query


async def asearch_graph_queries(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> Tuple[SearchGraphQueriesQueryOptions, ...]:
    """SearchGraphQueries

    List of all graph queries

    Arguments:
        search (Optional[str], optional): No description.
        values (Optional[List[ID]], optional): No description.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchGraphQueriesQueryGraphqueries]"""
    return (
        await aexecute(
            SearchGraphQueriesQuery, {"search": search, "values": values}, rath=rath
        )
    ).options


def search_graph_queries(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> Tuple[SearchGraphQueriesQueryOptions, ...]:
    """SearchGraphQueries

    List of all graph queries

    Arguments:
        search (Optional[str], optional): No description.
        values (Optional[List[ID]], optional): No description.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchGraphQueriesQueryGraphqueries]"""
    return execute(
        SearchGraphQueriesQuery, {"search": search, "values": values}, rath=rath
    ).options


async def aget_graph(id: ID, rath: Optional[KraphRath] = None) -> Graph:
    """GetGraph


    Arguments:
        id (ID): No description
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Graph"""
    return (await aexecute(GetGraphQuery, {"id": id}, rath=rath)).graph


def get_graph(id: ID, rath: Optional[KraphRath] = None) -> Graph:
    """GetGraph


    Arguments:
        id (ID): No description
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Graph"""
    return execute(GetGraphQuery, {"id": id}, rath=rath).graph


async def asearch_graphs(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> Tuple[SearchGraphsQueryOptions, ...]:
    """SearchGraphs

    List of all knowledge graphs

    Arguments:
        search (Optional[str], optional): No description.
        values (Optional[List[ID]], optional): No description.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchGraphsQueryGraphs]"""
    return (
        await aexecute(
            SearchGraphsQuery, {"search": search, "values": values}, rath=rath
        )
    ).options


def search_graphs(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> Tuple[SearchGraphsQueryOptions, ...]:
    """SearchGraphs

    List of all knowledge graphs

    Arguments:
        search (Optional[str], optional): No description.
        values (Optional[List[ID]], optional): No description.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchGraphsQueryGraphs]"""
    return execute(
        SearchGraphsQuery, {"search": search, "values": values}, rath=rath
    ).options


async def aget_protocol_step(id: ID, rath: Optional[KraphRath] = None) -> ProtocolStep:
    """GetProtocolStep


    Arguments:
        id (ID): No description
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        ProtocolStep"""
    return (await aexecute(GetProtocolStepQuery, {"id": id}, rath=rath)).protocol_step


def get_protocol_step(id: ID, rath: Optional[KraphRath] = None) -> ProtocolStep:
    """GetProtocolStep


    Arguments:
        id (ID): No description
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        ProtocolStep"""
    return execute(GetProtocolStepQuery, {"id": id}, rath=rath).protocol_step


async def asearch_protocol_steps(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> Tuple[SearchProtocolStepsQueryOptions, ...]:
    """SearchProtocolSteps

    List of all protocol steps

    Arguments:
        search (Optional[str], optional): No description.
        values (Optional[List[ID]], optional): No description.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchProtocolStepsQueryProtocolsteps]"""
    return (
        await aexecute(
            SearchProtocolStepsQuery, {"search": search, "values": values}, rath=rath
        )
    ).options


def search_protocol_steps(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> Tuple[SearchProtocolStepsQueryOptions, ...]:
    """SearchProtocolSteps

    List of all protocol steps

    Arguments:
        search (Optional[str], optional): No description.
        values (Optional[List[ID]], optional): No description.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchProtocolStepsQueryProtocolsteps]"""
    return execute(
        SearchProtocolStepsQuery, {"search": search, "values": values}, rath=rath
    ).options


async def aget_plot_view(id: ID, rath: Optional[KraphRath] = None) -> PlotView:
    """GetPlotView


    Arguments:
        id (ID): No description
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        PlotView"""
    return (await aexecute(GetPlotViewQuery, {"id": id}, rath=rath)).plot_view


def get_plot_view(id: ID, rath: Optional[KraphRath] = None) -> PlotView:
    """GetPlotView


    Arguments:
        id (ID): No description
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        PlotView"""
    return execute(GetPlotViewQuery, {"id": id}, rath=rath).plot_view


async def asearch_plot_views(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> Tuple[SearchPlotViewsQueryOptions, ...]:
    """SearchPlotViews

    List of all plot views

    Arguments:
        search (Optional[str], optional): No description.
        values (Optional[List[ID]], optional): No description.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchPlotViewsQueryPlotviews]"""
    return (
        await aexecute(
            SearchPlotViewsQuery, {"search": search, "values": values}, rath=rath
        )
    ).options


def search_plot_views(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> Tuple[SearchPlotViewsQueryOptions, ...]:
    """SearchPlotViews

    List of all plot views

    Arguments:
        search (Optional[str], optional): No description.
        values (Optional[List[ID]], optional): No description.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchPlotViewsQueryPlotviews]"""
    return execute(
        SearchPlotViewsQuery, {"search": search, "values": values}, rath=rath
    ).options


async def aget_node_category(
    id: ID, rath: Optional[KraphRath] = None
) -> Annotated[
    Union[
        GetNodeCategoryQueryNodecategoryBaseStructureCategory,
        GetNodeCategoryQueryNodecategoryBaseGenericCategory,
    ],
    Field(discriminator="typename"),
]:
    """GetNodeCategory


    Arguments:
        id (ID): No description
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        NodeCategory"""
    return (await aexecute(GetNodeCategoryQuery, {"id": id}, rath=rath)).node_category


def get_node_category(
    id: ID, rath: Optional[KraphRath] = None
) -> Annotated[
    Union[
        GetNodeCategoryQueryNodecategoryBaseStructureCategory,
        GetNodeCategoryQueryNodecategoryBaseGenericCategory,
    ],
    Field(discriminator="typename"),
]:
    """GetNodeCategory


    Arguments:
        id (ID): No description
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        NodeCategory"""
    return execute(GetNodeCategoryQuery, {"id": id}, rath=rath).node_category


async def aget_node_view(id: ID, rath: Optional[KraphRath] = None) -> NodeView:
    """GetNodeView


    Arguments:
        id (ID): No description
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        NodeView"""
    return (await aexecute(GetNodeViewQuery, {"id": id}, rath=rath)).node_view


def get_node_view(id: ID, rath: Optional[KraphRath] = None) -> NodeView:
    """GetNodeView


    Arguments:
        id (ID): No description
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        NodeView"""
    return execute(GetNodeViewQuery, {"id": id}, rath=rath).node_view


async def asearch_node_views(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> Tuple[SearchNodeViewsQueryOptions, ...]:
    """SearchNodeViews

    List of all node views

    Arguments:
        search (Optional[str], optional): No description.
        values (Optional[List[ID]], optional): No description.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchNodeViewsQueryNodeviews]"""
    return (
        await aexecute(
            SearchNodeViewsQuery, {"search": search, "values": values}, rath=rath
        )
    ).options


def search_node_views(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> Tuple[SearchNodeViewsQueryOptions, ...]:
    """SearchNodeViews

    List of all node views

    Arguments:
        search (Optional[str], optional): No description.
        values (Optional[List[ID]], optional): No description.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchNodeViewsQueryNodeviews]"""
    return execute(
        SearchNodeViewsQuery, {"search": search, "values": values}, rath=rath
    ).options


async def aget_measurment_category(
    id: ID, rath: Optional[KraphRath] = None
) -> MeasurementCategory:
    """GetMeasurmentCategory


    Arguments:
        id (ID): No description
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        MeasurementCategory"""
    return (
        await aexecute(GetMeasurmentCategoryQuery, {"id": id}, rath=rath)
    ).measurement_category


def get_measurment_category(
    id: ID, rath: Optional[KraphRath] = None
) -> MeasurementCategory:
    """GetMeasurmentCategory


    Arguments:
        id (ID): No description
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        MeasurementCategory"""
    return execute(
        GetMeasurmentCategoryQuery, {"id": id}, rath=rath
    ).measurement_category


async def asearch_measurment_category(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> Tuple[SearchMeasurmentCategoryQueryOptions, ...]:
    """SearchMeasurmentCategory

    List of all measurement categories

    Arguments:
        search (Optional[str], optional): No description.
        values (Optional[List[ID]], optional): No description.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchMeasurmentCategoryQueryMeasurementcategories]"""
    return (
        await aexecute(
            SearchMeasurmentCategoryQuery,
            {"search": search, "values": values},
            rath=rath,
        )
    ).options


def search_measurment_category(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> Tuple[SearchMeasurmentCategoryQueryOptions, ...]:
    """SearchMeasurmentCategory

    List of all measurement categories

    Arguments:
        search (Optional[str], optional): No description.
        values (Optional[List[ID]], optional): No description.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchMeasurmentCategoryQueryMeasurementcategories]"""
    return execute(
        SearchMeasurmentCategoryQuery, {"search": search, "values": values}, rath=rath
    ).options


async def aget_reagent(id: ID, rath: Optional[KraphRath] = None) -> Reagent:
    """GetReagent


    Arguments:
        id (ID): No description
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Reagent"""
    return (await aexecute(GetReagentQuery, {"id": id}, rath=rath)).reagent


def get_reagent(id: ID, rath: Optional[KraphRath] = None) -> Reagent:
    """GetReagent


    Arguments:
        id (ID): No description
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Reagent"""
    return execute(GetReagentQuery, {"id": id}, rath=rath).reagent


async def asearch_reagents(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> Tuple[SearchReagentsQueryOptions, ...]:
    """SearchReagents

    List of all reagents used in protocols

    Arguments:
        search (Optional[str], optional): No description.
        values (Optional[List[ID]], optional): No description.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchReagentsQueryReagents]"""
    return (
        await aexecute(
            SearchReagentsQuery, {"search": search, "values": values}, rath=rath
        )
    ).options


def search_reagents(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> Tuple[SearchReagentsQueryOptions, ...]:
    """SearchReagents

    List of all reagents used in protocols

    Arguments:
        search (Optional[str], optional): No description.
        values (Optional[List[ID]], optional): No description.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchReagentsQueryReagents]"""
    return execute(
        SearchReagentsQuery, {"search": search, "values": values}, rath=rath
    ).options


async def aget_node(
    id: ID, rath: Optional[KraphRath] = None
) -> Annotated[
    Union[GetNodeQueryNodeBaseEntity, GetNodeQueryNodeBaseStructure],
    Field(discriminator="typename"),
]:
    """GetNode


    Arguments:
        id (ID): No description
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Node"""
    return (await aexecute(GetNodeQuery, {"id": id}, rath=rath)).node


def get_node(
    id: ID, rath: Optional[KraphRath] = None
) -> Annotated[
    Union[GetNodeQueryNodeBaseEntity, GetNodeQueryNodeBaseStructure],
    Field(discriminator="typename"),
]:
    """GetNode


    Arguments:
        id (ID): No description
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Node"""
    return execute(GetNodeQuery, {"id": id}, rath=rath).node


async def asearch_entities(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> Tuple[SearchEntitiesQueryOptions, ...]:
    """SearchEntities

    List of all entities in the system

    Arguments:
        search (Optional[str], optional): No description.
        values (Optional[List[ID]], optional): No description.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchEntitiesQueryNodes]"""
    return (
        await aexecute(
            SearchEntitiesQuery, {"search": search, "values": values}, rath=rath
        )
    ).options


def search_entities(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> Tuple[SearchEntitiesQueryOptions, ...]:
    """SearchEntities

    List of all entities in the system

    Arguments:
        search (Optional[str], optional): No description.
        values (Optional[List[ID]], optional): No description.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchEntitiesQueryNodes]"""
    return execute(
        SearchEntitiesQuery, {"search": search, "values": values}, rath=rath
    ).options


async def aget_graph_view(id: ID, rath: Optional[KraphRath] = None) -> GraphView:
    """GetGraphView


    Arguments:
        id (ID): No description
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        GraphView"""
    return (await aexecute(GetGraphViewQuery, {"id": id}, rath=rath)).graph_view


def get_graph_view(id: ID, rath: Optional[KraphRath] = None) -> GraphView:
    """GetGraphView


    Arguments:
        id (ID): No description
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        GraphView"""
    return execute(GetGraphViewQuery, {"id": id}, rath=rath).graph_view


async def asearch_graph_views(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> Tuple[SearchGraphViewsQueryOptions, ...]:
    """SearchGraphViews

    List of all graph views

    Arguments:
        search (Optional[str], optional): No description.
        values (Optional[List[ID]], optional): No description.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchGraphViewsQueryGraphviews]"""
    return (
        await aexecute(
            SearchGraphViewsQuery, {"search": search, "values": values}, rath=rath
        )
    ).options


def search_graph_views(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> Tuple[SearchGraphViewsQueryOptions, ...]:
    """SearchGraphViews

    List of all graph views

    Arguments:
        search (Optional[str], optional): No description.
        values (Optional[List[ID]], optional): No description.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchGraphViewsQueryGraphviews]"""
    return execute(
        SearchGraphViewsQuery, {"search": search, "values": values}, rath=rath
    ).options


async def aget_ontology(id: ID, rath: Optional[KraphRath] = None) -> Ontology:
    """GetOntology


    Arguments:
        id (ID): No description
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Ontology"""
    return (await aexecute(GetOntologyQuery, {"id": id}, rath=rath)).ontology


def get_ontology(id: ID, rath: Optional[KraphRath] = None) -> Ontology:
    """GetOntology


    Arguments:
        id (ID): No description
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Ontology"""
    return execute(GetOntologyQuery, {"id": id}, rath=rath).ontology


async def asearch_ontologies(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> Tuple[SearchOntologiesQueryOptions, ...]:
    """SearchOntologies

    List of all ontologies

    Arguments:
        search (Optional[str], optional): No description.
        values (Optional[List[ID]], optional): No description.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchOntologiesQueryOntologies]"""
    return (
        await aexecute(
            SearchOntologiesQuery, {"search": search, "values": values}, rath=rath
        )
    ).options


def search_ontologies(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> Tuple[SearchOntologiesQueryOptions, ...]:
    """SearchOntologies

    List of all ontologies

    Arguments:
        search (Optional[str], optional): No description.
        values (Optional[List[ID]], optional): No description.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchOntologiesQueryOntologies]"""
    return execute(
        SearchOntologiesQuery, {"search": search, "values": values}, rath=rath
    ).options


GraphQueryInput.model_rebuild()
ProtocolStepInput.model_rebuild()
