"""Data modeling objects for creating corvic pipelines."""

import corvic.model._feature_type as feature_type
from corvic.model._agent import Agent, AgentID
from corvic.model._base_model import BaseModel, HasProtoSelf, UsesOrmID
from corvic.model._completion_model import (
    CompletionModel,
    CompletionModelID,
)
from corvic.model._feature_view import (
    Column,
    DeepGnnCsvUrlMetadata,
    FeatureView,
    FeatureViewEdgeTableMetadata,
    FeatureViewRelationshipsMetadata,
)
from corvic.model._pipeline import (
    ChunkPdfsPipeline,
    OcrPdfsPipeline,
    Pipeline,
    PipelineID,
    SanitizeParquetPipeline,
    SpecificPipeline,
    UnknownTransformationPipeline,
)
from corvic.model._proto_orm_convert import (
    UNCOMMITTED_ID_PREFIX,
    space_orm_to_proto,
    timestamp_orm_to_proto,
)
from corvic.model._resource import (
    Resource,
    ResourceID,
)
from corvic.model._room import (
    Room,
    RoomID,
)
from corvic.model._source import Source, SourceID
from corvic.model._space import (
    ConcatAndEmbedParameters,
    EmbedAndConcatParameters,
    EmbedImageParameters,
    ImageSpace,
    Node2VecParameters,
    RelationalSpace,
    SemanticSpace,
    Space,
    SpecificSpace,
    SpecificSpaceParameters,
    TabularSpace,
    UnknownSpace,
    embedding_model_proto_to_name,
    image_model_proto_to_name,
)

FeatureType = feature_type.FeatureType

__all__ = [
    "Agent",
    "AgentID",
    "BaseModel",
    "ChunkPdfsPipeline",
    "Column",
    "CompletionModel",
    "CompletionModelID",
    "ConcatAndEmbedParameters",
    "DeepGnnCsvUrlMetadata",
    "EmbedAndConcatParameters",
    "EmbedImageParameters",
    "FeatureType",
    "FeatureView",
    "FeatureViewEdgeTableMetadata",
    "FeatureViewRelationshipsMetadata",
    "HasProtoSelf",
    "ImageSpace",
    "Node2VecParameters",
    "OcrPdfsPipeline",
    "Pipeline",
    "PipelineID",
    "RelationalSpace",
    "Resource",
    "ResourceID",
    "Room",
    "RoomID",
    "SanitizeParquetPipeline",
    "SemanticSpace",
    "Source",
    "SourceID",
    "Space",
    "SpecificPipeline",
    "SpecificSpace",
    "SpecificSpaceParameters",
    "TabularSpace",
    "UNCOMMITTED_ID_PREFIX",
    "UnknownTransformationPipeline",
    "UnknownSpace",
    "UsesOrmID",
    "embedding_model_proto_to_name",
    "feature_type",
    "image_model_proto_to_name",
    "space_orm_to_proto",
    "timestamp_orm_to_proto",
]
