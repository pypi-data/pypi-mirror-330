#!/usr/bin/env python3
"""
MongoDB Schema Exporter

A tool to analyze MongoDB collections and generate schema definitions.
"""

import argparse
import sys
import pymongo
import pprint
import json
from typing import Any, Dict, List, Optional, cast
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.cursor import Cursor
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor

from .schema_types import MongoObject
from .schema_utils import (
    generate_schema,
    create_test_collection,
    validate_collection,
)


def main() -> int:
    """Main entry point for the MongoDB Schema Exporter."""
    parser = argparse.ArgumentParser(description="MongoDB Schema Exporter")
    parser.add_argument(
        "--uri", default="mongodb://localhost:27017/", help="MongoDB connection URI"
    )
    parser.add_argument("--db", required=True, help="Database name")
    parser.add_argument("--collection", required=True, help="Collection name")
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Number of documents to analyze (use 0 for all)",
    )
    parser.add_argument(
        "--output", choices=["pretty", "json"], default="pretty", help="Output format"
    )
    parser.add_argument("--output-file", help="Write output to file instead of stdout")
    parser.add_argument(
        "--keep-collection",
        action="store_true",
        help="Keep the collection after validation",
    )

    # Add validation options
    validation_group = parser.add_argument_group("validation")
    validation_group.add_argument(
        "--validate",
        action="store_true",
        help="Test if all documents in the collection comply with the generated schema",
    )

    args = parser.parse_args()

    client: pymongo.MongoClient = pymongo.MongoClient(
        args.uri, serverSelectionTimeoutMS=5000
    )
    client.server_info()  # Will raise an exception if cannot connect

    db: Database = client[args.db]
    collection: Collection = db[args.collection]

    # Get documents to analyze
    documents: Cursor
    total: int
    if args.limit > 0:
        documents = collection.find().limit(args.limit)
        total = args.limit
    else:
        documents = collection.find()
        total = collection.count_documents(filter={})

    if not documents:
        print(
            f"No documents found in collection {args.db}.{args.collection}",
            file=sys.stderr,
        )
        return 1

    print(f"Analyzing {total} documents from {args.db}.{args.collection}...")

    flattened_schema: MongoObject = MongoObject(fields={})
    buffer: List[Dict[str, Any]] = []
    executor: ProcessPoolExecutor = ProcessPoolExecutor(max_workers=10)

    for doc in tqdm(documents, desc="Generating schemas", unit="doc", total=total):
        buffer.append(doc)
        if len(buffer) == 100:
            # Cast the result to List[MongoObject] since we know all inputs are dicts
            object_schemas: List[MongoObject] = [
                cast(MongoObject, schema)
                for schema in executor.map(generate_schema, buffer)
            ]
            flattened_schema = MongoObject.merge(
                object_schemas + [flattened_schema]
            ).flatten()
            buffer.clear()

    if buffer:
        # Cast the result to List[MongoObject] since we know all inputs are dicts
        object_schemas = [
            cast(MongoObject, schema)
            for schema in executor.map(generate_schema, buffer)
        ]
        flattened_schema = MongoObject.merge(
            object_schemas + [flattened_schema]
        ).flatten()

    # Validate collection against schema if requested
    if args.validate:
        print(
            f"Validating documents in {args.db}.{args.collection} against generated schema..."
        )
        test_collection: Collection = create_test_collection(
            flattened_schema,
            client=client,
            db_name=f"{args.db}_validation",
            collection_name=f"{args.collection}_validation",
        )

        try:
            validate_collection(collection, test_collection, limit=args.limit)
        finally:
            if not args.keep_collection:
                test_collection.drop()
            else:
                print(
                    f"Keeping validation collection {args.db}_validation.{args.collection}_validation"
                )

        print("Validation complete!")

    # Output the schema
    output: Optional[str] = None
    if args.output == "pretty":
        output = pprint.pformat(flattened_schema)
    else:  # json
        schema_dict = flattened_schema.to_dict()
        output = json.dumps({"$jsonSchema": schema_dict}, indent=2)

    if args.output_file:
        with open(args.output_file, "w") as f:
            f.write(output)
        print(f"Schema written to {args.output_file}")
    else:
        print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main()) 