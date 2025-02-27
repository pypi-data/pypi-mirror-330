from ragloader.conf import Config
from ragloader.splitting import ChunkedDocument
from ragloader.embedding.mapper import EmbeddingModelsMapper
from ragloader.embedding import EmbeddedChunk, EmbeddedDocument


class DocumentEmbedder:
    """Class for embedding a chunked document."""

    def __init__(self, config: Config):
        self.embedding_model_name: str = config["pipeline_stages"]["embedding"]["embedding_model"]
        self.embedding_model = EmbeddingModelsMapper[self.embedding_model_name].value()

    def embed(self, chunked_document: ChunkedDocument):
        embedded_document: EmbeddedDocument = EmbeddedDocument(chunked_document)
        for chunk in chunked_document.chunks:
            embedded_chunk: EmbeddedChunk = self.embedding_model.embed(chunk)
            embedded_document.add_chunk(embedded_chunk)

        return embedded_document

    def __repr__(self):
        return f"DocumentEmbedder(model='{self.embedding_model_name}')"
