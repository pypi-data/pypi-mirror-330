import toml
from pathlib import Path
from pydantic import BaseModel, ValidationError

from ragloader.exceptions import InvalidConfigPath, InvalidConfigStructure


class ParsingConfig(BaseModel):
    label: str
    parsers: dict[str, str]

class ClassificationConfig(BaseModel):
    label: str
    categories: dict[str, list[str]]

class ExtractionConfig(BaseModel):
    label: str

class SplittingParams(BaseModel):
    chunk_size: int
    chunk_overlap: int

class SplittingConfig(BaseModel):
    label: str
    splitters: dict[str, str]
    splitters_params: dict[str, SplittingParams]

class EmbeddingConfig(BaseModel):
    label: str
    embedding_model: str

class QdrantConfig(BaseModel):
    location: str
    port: int

class DBConfig(BaseModel):
    qdrant: QdrantConfig

class PipelineStagesConfig(BaseModel):
    parsing: ParsingConfig
    classification: ClassificationConfig
    extraction: ExtractionConfig
    splitting: SplittingConfig
    embedding: EmbeddingConfig

class ConfigModel(BaseModel):
    pipeline_stages: PipelineStagesConfig
    db: DBConfig


class Config(dict):
    def __init__(self, config_path: Path | str = Path("ragloader/conf/config.toml")):
        try:
            with open(config_path, "r") as f:
                config = toml.load(f)
        except FileNotFoundError:
            raise InvalidConfigPath(f"Invalid path: {config_path}")

        try:
            config_model = ConfigModel(**config)
            super().__init__(config_model.model_dump())
        except ValidationError as e:
            raise InvalidConfigStructure(f"Invalid config structure: {e}")
