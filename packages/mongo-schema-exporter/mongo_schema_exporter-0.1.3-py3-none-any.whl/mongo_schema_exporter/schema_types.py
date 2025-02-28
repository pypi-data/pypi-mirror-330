"""
MongoDB schema type definitions.
This module contains classes that represent different MongoDB data types in a schema.
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Set, cast


@dataclass
class MongoType:
    """Base class for all MongoDB schema types."""

    def flatten(self) -> "MongoType":
        """
        Return a flattened version of this type, with any nested unions expanded.
        The default implementation returns the type as-is.
        """
        return self

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert this type to a dictionary for JSON serialization.
        This method should be implemented by subclasses.

        Returns:
            A dictionary representation of the type suitable for JSON serialization
        """
        raise NotImplementedError("Subclasses must implement to_dict")


@dataclass
class MongoScalar(MongoType):
    """Base class for all scalar MongoDB types."""

    pass


@dataclass
class MongoUnknown(MongoType):
    """Represents an unknown or unspecified MongoDB type."""

    def to_dict(self) -> Dict[str, Any]:
        return {}


@dataclass
class MongoNull(MongoScalar):
    """Represents a null value in MongoDB."""

    def to_dict(self) -> Dict[str, Any]:
        return {"bsonType": "null"}


@dataclass
class MongoString(MongoScalar):
    """Represents a string value in MongoDB."""

    def to_dict(self) -> Dict[str, Any]:
        return {"bsonType": "string"}


@dataclass
class MongoInteger(MongoScalar):
    """Represents an integer value in MongoDB."""

    def to_dict(self) -> Dict[str, Any]:
        return {"bsonType": "int"}


@dataclass
class MongoDouble(MongoScalar):
    """Represents a double value in MongoDB."""

    def to_dict(self) -> Dict[str, Any]:
        return {"bsonType": "double"}


@dataclass
class MongoObjectId(MongoScalar):
    """Represents a MongoDB ObjectId."""

    def to_dict(self) -> Dict[str, Any]:
        return {"bsonType": "objectId"}


@dataclass
class MongoBoolean(MongoScalar):
    """Represents a boolean value in MongoDB."""

    def to_dict(self) -> Dict[str, Any]:
        return {"bsonType": "bool"}


@dataclass
class MongoDate(MongoScalar):
    """Represents a date/datetime value in MongoDB."""

    def to_dict(self) -> Dict[str, Any]:
        return {"bsonType": "date"}


@dataclass
class MongoBinary(MongoScalar):
    """Represents a Binary data type in MongoDB."""

    def to_dict(self) -> Dict[str, Any]:
        return {"bsonType": "binary"}


@dataclass
class MongoDecimal128(MongoScalar):
    """Represents a Decimal128 number in MongoDB."""

    def to_dict(self) -> Dict[str, Any]:
        return {"bsonType": "decimal"}


@dataclass
class MongoRegex(MongoScalar):
    """Represents a regular expression in MongoDB."""

    def to_dict(self) -> Dict[str, Any]:
        return {"bsonType": "regex"}


@dataclass
class MongoTimestamp(MongoScalar):
    """Represents a timestamp in MongoDB."""

    def to_dict(self) -> Dict[str, Any]:
        return {"bsonType": "timestamp"}


@dataclass
class MongoField:
    """
    Represents a field in a MongoDB document.

    Attributes:
        type: The type of the field
        required: Whether the field is required (true) or optional (false)
    """

    type: MongoType
    required: bool


@dataclass
class MongoObject(MongoType):
    """
    Represents a MongoDB document or embedded document (object).

    Attributes:
        fields: A dictionary mapping field names to their types and requirements
    """

    fields: Dict[str, MongoField]

    def flatten(self) -> "MongoObject":
        return MongoObject(
            fields={
                k: MongoField(type=v.type.flatten(), required=v.required)
                for k, v in self.fields.items()
            }
        )

    def to_dict(self) -> Dict[str, Any]:
        properties = {}
        required = []
        for key, field in self.fields.items():
            properties[key] = field.type.to_dict()
            if field.required:
                required.append(key)
        result = {"bsonType": "object", "properties": properties}
        if required:
            result["required"] = required
        return result

    @staticmethod
    def merge(objects: list["MongoObject"]) -> "MongoObject":
        """
        Merge multiple object types into a single object type.
        Fields present in any object will be included in the result.
        Field types are merged using union if they differ between objects.
        Fields are marked as required only if they appear in all objects and are
        required in all of those instances.

        Args:
            objects: A list of MongoObject instances to merge

        Returns:
            A new MongoObject with merged fields
        """
        if len(objects) == 0:
            return MongoObject(fields={})
        elif len(objects) == 1:
            return objects[0]

        # First collect all fields from all objects
        all_keys: Set[str] = set()
        for o in objects:
            all_keys.update(o.fields.keys())

        # Count how many objects each key appears in
        key_count = {key: 0 for key in all_keys}
        for o in objects:
            for key in o.fields:
                key_count[key] += 1

        fields: Dict[str, MongoField] = dict()
        for o in objects:
            for key, field in o.fields.items():
                if key not in fields:
                    # Field should only be required if it appears in all objects
                    is_required = key_count[key] == len(objects) and field.required
                    fields[key] = MongoField(type=field.type, required=is_required)
                else:
                    current = fields[key]
                    is_required = (
                        key_count[key] == len(objects)
                        and current.required
                        and field.required
                    )
                    if current.type != field.type:
                        fields[key] = MongoField(
                            type=MongoUnion(types=[current.type, field.type]).flatten(),
                            required=is_required,
                        )
                    else:
                        fields[key] = MongoField(
                            type=current.type,
                            required=is_required,
                        )

        return MongoObject(fields=fields)


@dataclass
class MongoArray(MongoType):
    """Represents an array/list in MongoDB."""

    element: MongoType

    def flatten(self) -> MongoType:
        return MongoArray(element=self.element.flatten())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "bsonType": "array",
            "items": self.element.to_dict(),
        }

    @staticmethod
    def merge(arrays: List["MongoArray"]) -> "MongoArray":
        """
        Merge multiple array types into a single array type.
        The element type of the resulting array is the union of all input element types.

        Args:
            arrays: A list of MongoArray objects to merge

        Returns:
            A new MongoArray with element type being the union of all input element types
        """
        if len(arrays) == 0:
            return MongoArray(element=MongoUnknown())

        return MongoArray(
            element=MongoUnion(types=[a.element for a in arrays]).flatten()
        )


@dataclass
class MongoUnion(MongoType):
    """
    Represents a union of multiple MongoDB types.
    This occurs when a field can contain values of different types.
    """

    types: List[MongoType]

    def flatten(self) -> MongoType:
        """
        Flatten this union type by expanding any nested unions,
        merging arrays and objects.
        Empty unions become MongoUnknown, and single-element unions
        are replaced with their contained type.
        """
        if len(self.types) == 0:
            return MongoUnknown()

        if len(self.types) == 1:
            return self.types[0]

        flattened_types: List[MongoType] = [t.flatten() for t in self.types]

        expanded_unions_types: List[MongoType] = list()
        for t in flattened_types:
            if isinstance(t, MongoUnion):
                expanded_unions_types.extend(t.types)
            else:
                expanded_unions_types.append(t)

        unique_types: List[MongoType] = list()
        for t in expanded_unions_types:
            if t not in unique_types:
                unique_types.append(t)

        objects: List[MongoObject] = list()
        arrays: List[MongoArray] = list()
        scalars: List[MongoScalar] = list()

        for t in unique_types:
            if isinstance(t, MongoObject):
                objects.append(t)
            elif isinstance(t, MongoArray):
                arrays.append(t)
            elif isinstance(t, MongoScalar):
                scalars.append(t)
            elif isinstance(t, MongoUnknown):
                pass
            else:
                raise ValueError(f"Unknown type: {type(t)}")

        resulting_types: List[MongoType] = []
        # Convert scalars list to List[MongoType] to fix the variance issue
        resulting_types.extend(cast(List[MongoType], scalars))

        if arrays:
            resulting_types.append(MongoArray.merge(arrays))

        if objects:
            resulting_types.append(MongoObject.merge(objects))

        return MongoUnion(types=resulting_types)

    def to_dict(self) -> Dict[str, Any]:
        if len(self.types) == 0:
            return {}

        if len(self.types) == 1:
            return self.types[0].to_dict()

        if all(isinstance(t, MongoScalar) for t in self.types):
            return {"bsonType": [t.to_dict()["bsonType"] for t in self.types]}
        else:
            return {"oneOf": [t.to_dict() for t in self.types]}
