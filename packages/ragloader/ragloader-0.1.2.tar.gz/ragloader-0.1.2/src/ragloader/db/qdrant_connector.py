from typing import Literal
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Record
from qdrant_client.models import VectorParams, Distance

from ragloader.exceptions import QdrantCollectionExists


class QdrantConnector:
    """This class provides an abstraction layer over the Python Qdrant client"""
    def __init__(self, db_config: dict):
        self.db_config: dict = db_config
        self.client = QdrantClient(**self.db_config)

    def create_collection(
        self,
        collection_name: str,
        vectors_length: int | None = None,
        if_exists: Literal["fail", "replace", "ignore"] = "replace"
    ):
        """
        Creates a new Qdrant collection

        Args:
            collection_name (str): The name of the new collection
            vectors_length (int | None): Required by `create_collection()` from `qdrant_client`
            if_exists (Literal["fail", "replace", "ignore"]):
                How to handle creating an existing collection

        Returns:
            (bool): Whether the collection was created successfully

        Raises:
            QdrantCollectionExists: The collection already exists
            ValueError: Invalid `if_exists` value
        """

        if vectors_length is None:
            vectors_config = {}
        elif isinstance(vectors_length, int) and vectors_length > 0:
            vectors_config = VectorParams(size=vectors_length, distance=Distance.COSINE)
        else:
            raise ValueError(f"Invalid `vectors_length` value: {vectors_length}")

        if vectors_config is not None:
            vectors_config = VectorParams(size=768, distance=Distance.COSINE)

        if self.client.collection_exists(collection_name):
            if if_exists == "fail":
                raise QdrantCollectionExists(f"Collection '{collection_name}' already exists")
            elif if_exists == "replace":
                if self.client.collection_exists(collection_name):
                    self.client.delete_collection(collection_name)
                self.client.create_collection(collection_name, vectors_config)
                return True
            elif if_exists == "ignore":
                return False
            else:
                raise ValueError(f"Invalid 'if_exists' value: {if_exists}")
        else:
            self.client.create_collection(collection_name, vectors_config)
            return True

    def add_record(self, collection_name: str, point: PointStruct):
        """
        Adds a record to the existing collection.

        Args:
            collection_name (str): The name of the collection
            point (PointStruct): The point to be added

        Returns:
            (bool): Whether the record was added successfully
        """
        try:
            self.client.upsert(
                collection_name=collection_name,
                points=[point]
            )
            return True
        except Exception as e:
            # TODO logging
            return False

    def get_records(self, collection_name: str) -> list[Record]:
        records = self.client.scroll(collection_name)[0]
        return records

    def __repr__(self):
        return f"QdrantConnector({self.db_config})"


if __name__ == "__main__":
    qc = QdrantConnector({"location": "localhost", "port": 6333})

    for collection in qc.client.get_collections().collections:
        qc.client.delete_collection(collection.name)
