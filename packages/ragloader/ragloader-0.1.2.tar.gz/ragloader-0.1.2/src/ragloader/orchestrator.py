import threading
from pathlib import Path
from qdrant_client.models import PointStruct
from concurrent.futures import ThreadPoolExecutor

from ragloader.conf import Config
from ragloader.db import QdrantConnector
from ragloader.indexing import DocumentsStructure, FilesIndexer, Document
from ragloader.parsing import DocumentParser, ParsedDocument
from ragloader.classification import DocumentClassifier, ClassifiedDocument
from ragloader.extraction import DocumentExtractor, ExtractedDocument
from ragloader.splitting import DocumentSplitter, ChunkedDocument
from ragloader.embedding import DocumentEmbedder, EmbeddedDocument


class UploadOrchestrator:
    def __init__(self, data_directory: Path | str, config: Config | Path | str | None = None):
        if config is None:
            self.config: Config = Config()
        elif isinstance(config, (str, Path)):
            self.config: Config = Config(Path(config))
        elif isinstance(config, Config):
            self.config: Config = config
        else:
            raise TypeError(f"Invalid type for config: {type(config)}")

        self.data_directory: Path = Path(data_directory)
        self.documents_structure: DocumentsStructure | None = None

        self.lock = threading.Lock()
        self.qdrant: QdrantConnector = QdrantConnector(self.config["db"]["qdrant"])

        self.document_parser: DocumentParser = DocumentParser(self.config)
        self.document_classifier: DocumentClassifier = DocumentClassifier(self.config)
        self.document_extractor: DocumentExtractor = DocumentExtractor(self.config)
        self.document_splitter: DocumentSplitter = DocumentSplitter(self.config)
        self.document_embedder: DocumentEmbedder = DocumentEmbedder(self.config)

        self.stages: list[str] = list(self.config["pipeline_stages"].keys())
        self.collection_names: dict[str, str] = dict().fromkeys(self.stages)
        self.initialize_collections()

    def initialize_collections(self):
        collections_names_base = ["parsed_files", "classified_documents",
                                  "extracted_documents", "chunked_documents"]
        for base_name, stage in zip(collections_names_base, self.stages):
            collection_name = f"{self.config['pipeline_stages'][stage]['label']}__{base_name}"
            self.collection_names[stage] = collection_name
            self.qdrant.create_collection(collection_name, if_exists="ignore")

        embedding_label = self.config["pipeline_stages"]["embedding"]["label"]
        embeddings_collection_name = f"{embedding_label}__embedded_chunks"
        self.collection_names["embedding"] = embeddings_collection_name
        self.qdrant.create_collection(
            embeddings_collection_name,
            vectors_length=self.document_embedder.embedding_model.vector_length,
            if_exists="ignore",
        )

    def upload(self):
        self.index_files()
        documents: list[Document] = [
            document for group in self.documents_structure.groups for document in group.documents
        ]

        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(self.pipeline, document) for document in documents]
            for future in futures:
                future.result()

    def pipeline(self, document: Document):
        parsed_document: ParsedDocument = self.parse_document(document)
        classified_document: ClassifiedDocument = self.classify_document(parsed_document)
        extracted_document: ExtractedDocument = self.extract_content(classified_document)
        chunked_document: ChunkedDocument = self.split_document(extracted_document)
        self.embed_document(chunked_document)

    def index_files(self):
        indexer = FilesIndexer(self.data_directory)
        self.documents_structure = indexer.scan()

    def parse_document(self, document: Document) -> ParsedDocument:
        parsed_document: ParsedDocument = self.document_parser.parse(document)

        if parsed_document is not None:
            for file_idx, parsed_file in enumerate(parsed_document.parsed_files):
                payload: dict = {
                    "file_path": parsed_file.file_path,
                    "file_name": parsed_file.file_name,
                    "file_extension": parsed_file.extension,
                    "document_uuid": parsed_document.uuid,
                    "group_name": parsed_document.group,
                    "file_content": parsed_file.file_content,
                }
                point: PointStruct = PointStruct(
                    id=str(parsed_file.uuid), vector={}, payload=payload)
                with self.lock:
                    self.qdrant.add_record(self.collection_names["parsing"], point)

        return parsed_document

    def classify_document(self, parsed_document: ParsedDocument) -> ClassifiedDocument:
        classified_document: ClassifiedDocument = self.document_classifier.classify(parsed_document)

        # TODO add classified_document to the db

        return classified_document

    def extract_content(self, classified_document: ClassifiedDocument) -> ExtractedDocument:
        extracted_document: ExtractedDocument = self.document_extractor.extract(classified_document)

        # TODO add extracted_document to the db

        return extracted_document

    def split_document(self, extracted_document: ExtractedDocument) -> ChunkedDocument:
        """
        Splits an extracted_document into a chunked document.
        Chunks of a given document are stored in a list of dictionaries, where each dictionary contains:
        - chunk_index: index of the chunk in the document
        - content: text content of the chunk
        - metadata: metadata of the chunk
        """
        chunked_document: ChunkedDocument = self.document_splitter.split(extracted_document)

        point: PointStruct = PointStruct(id=str(chunked_document.uuid),
                                         vector={}, payload=chunked_document.db_payload)
        with self.lock:
            self.qdrant.add_record(self.collection_names["splitting"], point)

        return chunked_document

    def embed_document(self, chunked_document: ChunkedDocument):
        embedded_document: EmbeddedDocument = self.document_embedder.embed(chunked_document)

        for embedded_chunk in embedded_document.embedded_chunks:
            point: PointStruct = PointStruct(
                id=str(embedded_chunk.uuid), vector=embedded_chunk.embedding,
                payload=embedded_chunk.payload
            )
            with self.lock:
                self.qdrant.add_record(self.collection_names["embedding"], point)

        return embedded_document


if __name__ == "__main__":
    root_path = "../../data/"

    orchestrator = UploadOrchestrator(root_path, "conf/config.toml")
    orchestrator.upload()
