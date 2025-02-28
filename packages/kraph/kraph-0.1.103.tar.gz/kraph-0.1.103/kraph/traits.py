from pydantic import BaseModel
from typing import TYPE_CHECKING, Any, Optional
from kraph.vars import current_ontology, current_graph
import dataclasses
import datetime
from rath.turms.utils import NotQueriedError, get_attributes_or_error


if TYPE_CHECKING:
    from kraph.api.schema import Entity


@dataclasses.dataclass
class MeasurementWithValue:
    measurement: "MeasurementCategoryTrait"
    value: float
    valid_from: Optional[datetime.datetime] = None
    valid_to: Optional[datetime.datetime] = None
    
    def __ror__(self, other):
        from rekuest_next.structures.default import get_default_structure_registry
        from kraph.api.schema import create_structure
    
        
        if isinstance(other, BaseModel):
            registry = get_default_structure_registry()
            graph = current_graph.get()            
            return IntermediateMeasurement(left=create_structure(other, graph), measurement_with_value=self)
            
        raise NotImplementedError("You can only merge a measurement with a structure")


@dataclasses.dataclass
class IntermediateRelation:
    left: "EntityTrait"
    kind: "RelationCategoryTrait"

    def __or__(self, other):
        from kraph.api.schema import create_relation

        if isinstance(other, EntityTrait):
            return create_relation(left=self.left, right=other, kind=self.kind)
        raise NotImplementedError


@dataclasses.dataclass
class RelationWithValidity:
    relation: "RelationCategoryTrait"
    value: float
    valid_from: Optional[datetime.datetime] = None
    valid_to: Optional[datetime.datetime] = None


@dataclasses.dataclass
class IntermediateMeasurement:
    left: "EntityTrait"
    measurement_with_value: "MeasurementWithValue"

    def __or__(self, other):
        from kraph.api.schema import create_measurement

        if isinstance(other, EntityTrait):
            return create_measurement(
                self.left,
                other,
                expression=self.measurement_with_value.measurement,
                value=self.measurement_with_value.value,
                valid_from=self.measurement_with_value.valid_from,
                valid_to=self.measurement_with_value.valid_to,
            )

        raise NotImplementedError


@dataclasses.dataclass
class IntermediateRelationWithValidity:
    left: "EntityTrait"
    relation_with_validity: RelationWithValidity

    def __or__(self, other):
        from kraph.api.schema import create_relation

        if isinstance(other, EntityTrait):
            return create_relation(
                self.left,
                other,
                self.relation_with_validity.relation,
                valid_from=self.relation_with_validity.valid_from,
                valid_to=self.relation_with_validity.valid_to,
            )

        raise NotImplementedError


class EntityTrait(BaseModel):
    def __or__(self, other):
        if other is None:
            return self

        if isinstance(other, StructureTrait):
            raise NotImplementedError(
                "Cannot merge structures directly, use a relation or measurement inbetween"
            )

        if isinstance(other, EntityTrait):
            raise NotImplementedError(
                "Cannot merge structure and entities directly, use a relation or measurement inbetween"
            )

        if isinstance(other, MeasurementCategoryTrait):
            raise NotImplementedError(
                "When merging a structure and a measurement, please instatiante the measurement with a value first"
            )

        if isinstance(other, RelationCategoryTrait):
            return IntermediateRelation(self, other)


class StructureTrait(BaseModel):
    def __or__(self, other):
        if other is None:
            return self

        if isinstance(other, StructureTrait):
            raise NotImplementedError(
                "Cannot merge structures directly, use a relation or measurement inbetween"
            )

        if isinstance(other, EntityTrait):
            raise NotImplementedError(
                "Cannot merge structure and entities directly, use a relation or measurement inbetween"
            )

        if isinstance(other, MeasurementCategoryTrait):
            raise NotImplementedError(
                "When merging a structure and a measurement, please instatiante the measurement with a value first"
            )

        if isinstance(other, RelationCategoryTrait):
            return

        raise NotImplementedError
    
    

class RelationCategoryTrait(BaseModel):

    def __str__(self):
        return get_attributes_or_error(self, "age_name")
    
    def __or__(self, other):
        raise NotImplementedError

    def __call__(self, valid_from=None, valid_to=None):
        return RelationWithValidity(kind=self, valid_from=valid_from, valid_to=valid_to)


class MeasurementCategoryTrait(BaseModel):

    def __str__(self):
        return get_attributes_or_error(self, "age_name")
    
    
    def __call__(self, value, valid_from=None, valid_to=None):
        from kraph.api.schema import MeasurementKind

        try:
            kind = get_attributes_or_error(self, "category.metric_kind")
        except NotQueriedError:
            kind = None
            
        if kind:
            if kind == MeasurementKind.FLOAT:
                assert isinstance(value, float), "Value must be a float"
            elif kind == MeasurementKind.INT:
                assert isinstance(value, int), "Value must be an int"
            elif kind == MeasurementKind.STRING:
                assert isinstance(value, str), "Value must be a string"
            elif kind == MeasurementKind.BOOL:
                assert isinstance(value, bool), "Value must be a bool"
            else:
                raise NotImplementedError(f"Kind {kind} not implemented")

        return MeasurementWithValue(
            measurement=self, value=value, valid_from=valid_from, valid_to=valid_to
        )





class StructureCategoryTrait(BaseModel):

    def __str__(self):
        return get_attributes_or_error(self, "age_name")
     

    def __or__(self, other):
        raise NotImplementedError("You cannot relate structure categories directly. Use a entitiy instead")

    def create_structure(self, identifier) -> "Entity":
        from kraph.api.schema import create_structure

        """Creates an entity with a name


        """
        graph = current_graph.get()
        return create_structure(identifier, graph)

    def __call__(self, *args, **kwds):
        return self.create_structure(*args, **kwds)



class GenericCategoryTrait(BaseModel):
    """Allows for the creation of a generic category"""

    def __str__(self):
        return get_attributes_or_error(self, "age_name")
    
    def __or__(self, other):
        raise NotImplementedError("You cannot relate structure categories directly. Use an entitiy instead E.g. by calling the category")

    def create_entity(self, *args, **kwargs) -> "Entity":
        from kraph.api.schema import create_entity

        """Creates an entity with a name


        """
        graph = current_graph.get()
        id = get_attributes_or_error(self, "id")
        return create_entity(graph, id)

    def __call__(self, *args, **kwargs):
        return self.create_entity(*args, **kwargs)



class ExpressionTrait(BaseModel):
    def __or__(self, other):
        raise NotImplementedError

    def __str__(self):
        return getattr(self, "label", super().__str__())


class EntityTrait(BaseModel):
    
    
    def __or__(self, other):
        if isinstance(other, MeasurementWithValue):
            return IntermediateMeasurement(left=self, measurment=other)
        if isinstance(other, RelationWithValidity):
            return IntermediateRelationWithValidity(left=self, relation_with_validity=other)
        if isinstance(other, EntityTrait):
            raise NotImplementedError("Cannot merge entities directly, use a relation or measurement inbetween")
        if isinstance(other, StructureTrait):
            raise NotImplementedError("Cannot merge entities and structures directly, use a relation or measurement inbetween")
        if isinstance(other, RelationCategoryTrait):
            return IntermediateRelation(self, other)
        if isinstance(other, MeasurementCategoryTrait):
            raise NotImplementedError("When merging a entity and a measurement, please instatiante the measurement with a value first")

    def set(self, metric: "LinkedExpressionTrait", value: float, **kwargs):
        from kraph.api.schema import create_entity_metric, ExpressionKind

        assert isinstance(
            metric, LinkedExpressionTrait
        ), "Metric must be a LinkedExpressionTrait"
        (
            get_attributes_or_error(metric, "kind") == ExpressionKind.METRIC,
            "Expression must be a METRIC",
        )

        return create_entity_metric(entity=self, metric=metric, value=value, **kwargs)

    def subject_to(self, **kwargs):
        from kraph.api.schema import (
            create_protocol_step,
            ProtocolStepInput,
            ExpressionKind,
        )

        return create_protocol_step(input=ProtocolStepInput(entity=self, **kwargs))



class OntologyTrait(BaseModel):
    _token = None

    def __enter__(self):
        self._token = current_ontology.set(self)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        current_ontology.reset(self._token)


class GraphTrait(BaseModel):
    _token = None

    def __enter__(self):
        self._token = current_graph.set(self)
        self._ontotoken = current_ontology.set(self.ontology)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        current_graph.reset(self._token)
        current_ontology.reset(self._ontotoken)


class HasPresignedDownloadAccessor(BaseModel):
    _dataset: Any = None

    def download(self, file_name: str = None) -> "str":
        from kraph.io import download_file

        url, key = get_attributes_or_error(self, "presigned_url", "key")
        return download_file(url, file_name=file_name or key)
