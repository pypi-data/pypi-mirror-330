"""
Utility functions for MongoDB schema operations.
This module contains helper functions for schema generation, merging, and conversion.
"""

from typing import Any, Dict, List, TypeVar
from bson import ObjectId, Decimal128, Binary, Timestamp, Regex
from datetime import datetime
import pymongo
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.cursor import Cursor
from tqdm import tqdm

from .schema_types import (
    MongoType,
    MongoUnknown,
    MongoString,
    MongoInteger,
    MongoDouble,
    MongoBoolean,
    MongoDate,
    MongoObjectId,
    MongoNull,
    MongoUnion,
    MongoArray,
    MongoObject,
    MongoField,
    MongoBinary,
    MongoDecimal128,
    MongoRegex,
    MongoTimestamp,
)


T = TypeVar("T")


def generate_schema(value: Any) -> MongoType:
    """
    Generate a schema type representation for a MongoDB value.

    This function recursively analyzes values and generates appropriate schema types:
    - Scalar types (str, int, float, bool, ObjectId, etc.) become their respective types
    - Lists become MongoArray types with element types determined from the list items
    - Dictionaries become MongoObject types with fields corresponding to the dict keys

    Args:
        value: A MongoDB value to analyze

    Returns:
        A MongoType representing the schema of the value
        (For dictionaries, returns MongoObject specifically)

    Raises:
        ValueError: If the value is of an unsupported type
    """
    if isinstance(value, bool):
        return MongoBoolean()
    elif isinstance(value, int):
        return MongoInteger()
    elif isinstance(value, float):
        return MongoDouble()
    elif isinstance(value, ObjectId):
        return MongoObjectId()
    elif isinstance(value, datetime):
        return MongoDate()
    elif isinstance(value, Binary):
        return MongoBinary()
    elif isinstance(value, Decimal128):
        return MongoDecimal128()
    elif isinstance(value, Regex):
        return MongoRegex()
    elif isinstance(value, Timestamp):
        return MongoTimestamp()
    elif isinstance(value, str):
        return MongoString()
    elif isinstance(value, list):
        if not value:  # Empty list
            return MongoArray(element=MongoUnknown())
        return MongoArray(
            element=MongoUnion(
                types=[generate_schema(item) for item in value]
            ).flatten()
        )
    elif isinstance(value, dict):
        # For dictionaries, we specifically return MongoObject (important for type narrowing)
        result: MongoObject = MongoObject(
            fields={
                k: MongoField(type=generate_schema(v), required=True)
                for k, v in value.items()
            }
        )
        return result
    elif value is None:
        return MongoNull()
    else:
        raise ValueError(f"Unknown type: {type(value)}")


def create_test_collection(
    schema: MongoType,
    client: pymongo.MongoClient,
    db_name: str = "test_validation",
    collection_name: str = "test_collection",
) -> Collection:
    """
    Create a test collection with schema validation applied.

    Args:
        schema: The schema to use for validation
        client: Optional pymongo client, if None a new client will be created
        db_name: Database name (default: 'test_validation')
        collection_name: Collection name (default: 'test_collection')

    Returns:
        The created collection with validation rules applied
    """
    # Drop collection if it exists
    db: Database = client[db_name]
    if collection_name in db.list_collection_names():
        db.drop_collection(collection_name)

    # Create new collection
    db.create_collection(collection_name)
    collection: Collection = db[collection_name]

    # Apply schema validation
    schema_dict: Dict[str, Any] = schema.to_dict()
    validator: Dict[str, Any] = {"$jsonSchema": schema_dict}

    db.command(
        "collMod",
        collection_name,
        validator=validator,
        validationLevel="strict",
        validationAction="error",
    )

    return collection


def validate_collection(source: Collection, target: Collection, batch_size: int, limit: int) -> None:
    """
    Copy documents from source to target collection, throwing validation errors.
    The target collection should have validation rules applied.

    Args:
        source: Source collection to copy from
        target: Target collection with validation rules
        limit: Maximum number of documents to validate (0 for all)
    """
    documents: Cursor
    total: int

    if limit > 0:
        documents = source.find().sort([("_id", pymongo.DESCENDING)]).limit(limit)
        total = limit
    else:
        documents = source.find()
        total = source.count_documents(filter={})

    buffer: List[Dict[str, Any]] = []
    for doc in tqdm(documents.batch_size(batch_size), desc="Validating documents", unit="doc", total=total):
        buffer.append(doc)
        if len(buffer) == 100:
            target.insert_many(buffer)
            buffer.clear()

    if buffer:
        target.insert_many(buffer)
