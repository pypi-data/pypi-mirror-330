import io
from typing import IO, List, Union, Any, Tuple
from graphql import (
    DocumentNode,
    parse,
    OperationDefinitionNode,
    OperationType,
    print_ast,
    print_source_location,
    print_location,
    GraphQLError,
)
from graphql.language.print_location import print_prefixed_lines
from pydantic import BaseModel
from typing import Any, Callable, Generator, Type


class RemoteUpload:
    """A custom scalar for wrapping of every supported array like structure on
    the mikro platform. This scalar enables validation of various array formats
    into a mikro api compliant xr.DataArray.."""

    def __init__(self, value: IO) -> None:
        self.value = value
        self.key = str(value.name)

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, *info):
        """Validate the input array and convert it to a xr.DataArray."""

        if isinstance(v, str):
            v = open(v, "rb")

        if not isinstance(v, io.IOBase):
            raise ValueError("This needs to be a instance of a file")

        return cls(v)

    def __repr__(self):
        return f"RemoteUpload({self.value})"


class NodeID(str):
    def to_graph_id(self):
        return self.split(":")[1]

    def to_graph_name(self):
        return self.split(":")[0]

    @classmethod
    def __get_validators__(
        cls: Type["NodeID"],
    ) -> Generator[Callable[..., Any], Any, Any]:
        """Get validators"""
        # one or more validators may be yielded which will be called in the
        # order to validate the input, each validator will receive as an input
        # the value returned from the previous validator
        yield cls.validate

    @classmethod
    def validate(cls: Type["NodeID"], v: Any, *info) -> "NodeID":
        """Validate the ID"""
        if isinstance(v, BaseModel):
            if hasattr(v, "id"):
                return cls(v.id)  # type: ignore
            else:
                raise TypeError("This needs to be a instance of BaseModel with an id")

        if isinstance(v, str):
            return cls(v)

        if isinstance(v, int):
            return cls(str(v))

        raise TypeError(
            "Needs to be either a instance of BaseModel (with an id) or a string"
        )


class StructureIdentifier(str):
    def to_graph_id(self):
        return self.split(":")[1]

    def to_graph_name(self):
        return self.split(":")[0]

    @classmethod
    def __get_validators__(
        cls: Type["NodeID"],
    ) -> Generator[Callable[..., Any], Any, Any]:
        """Get validators"""
        # one or more validators may be yielded which will be called in the
        # order to validate the input, each validator will receive as an input
        # the value returned from the previous validator
        yield cls.validate

    @classmethod
    def validate(cls: Type["NodeID"], v: Any, *info) -> "NodeID":
        """Validate the ID"""
        
        
        if isinstance(v, BaseModel):
            from rekuest_next.structures.default import get_default_structure_registry

            registry = get_default_structure_registry()
            print(registry)

            identifier = registry.get_identifier_for_cls(v.__class__)
            return identifier

        if isinstance(v, str):
            assert "@" in v, "The string needs to be a valid identifier"
            return cls(v)

        if isinstance(v, int):
            return cls(str(v))

        raise TypeError(
            "Needs to be either a instance of BaseModel (with an id) or a string"
        )


class StructureString(str):
    def to_graph_id(self):
        return self.split(":")[1]

    def to_graph_name(self):
        return self.split(":")[0]

    @classmethod
    def __get_validators__(
        cls: Type["NodeID"],
    ) -> Generator[Callable[..., Any], Any, Any]:
        """Get validators"""
        # one or more validators may be yielded which will be called in the
        # order to validate the input, each validator will receive as an input
        # the value returned from the previous validator
        yield cls.validate

    @classmethod
    def validate(cls: Type["NodeID"], v: Any, *info) -> "NodeID":
        """Validate the ID"""
        if isinstance(v, BaseModel):
            from rekuest_next.structures.default import get_default_structure_registry

            registry = get_default_structure_registry()
            identifier = registry.get_identifier_for_cls(v.__class__)
            assert hasattr(v, "id"), "The structure needs to have an id"

            return f"{identifier}:{v.id}"

        if isinstance(v, str):
            assert "@" in v, "The string needs to be a valid identifier"
            return cls(v)

        if isinstance(v, int):
            return cls(str(v))

        raise TypeError(
            "Needs to be either a instance of BaseModel (with an id) or a string"
        )


class Cypher(str):
    def to_graph_id(self):
        return self.split(":")[1]

    def to_graph_name(self):
        return self.split(":")[0]

    @classmethod
    def __get_validators__(
        cls: Type["NodeID"],
    ) -> Generator[Callable[..., Any], Any, Any]:
        """Get validators"""
        # one or more validators may be yielded which will be called in the
        # order to validate the input, each validator will receive as an input
        # the value returned from the previous validator
        yield cls.validate

    @classmethod
    def validate(cls: Type["NodeID"], v: Any, *info) -> "NodeID":
        if isinstance(v, str):
            return cls(v)
        raise TypeError("Needs to be either str or a string")
