from enum import Enum

from .embedders.paraphrase_multilingual_mpnet import ParaphraseMultilingualMpnet


class EmbeddingModelsMapper(Enum):
    """Mapper from embedding models' names and embedding models."""
    paraphrase_multilingual_mpnet = ParaphraseMultilingualMpnet
