from typing import Dict, List, Literal, Optional, Union

from api_schemas.base import BaseInputModel
from api_schemas.embedding import ExecutorUsage, TextDoc, Usage
from docarray import BaseDoc, DocList
from docarray.base_doc.doc import BaseDocWithoutId
from docarray.typing import NdArray
from pydantic import Field


## Model to be imported by the Executor and used by the Universal API to communicate with it # noqa
class ChunkedEmbeddingsDoc(BaseDoc):
    """Document to be returned by the embedding backend, containing the embedding
    vector and the token usage for the corresponding input texts"""

    embeddings: NdArray = Field(
        description='A tensor of embeddings for the text', default=[]
    )
    usage: ExecutorUsage
    chunks: List[str]
    # truncated: Optional[bool] = Field(
    #     description='Flag to inform that the embedding is computed ', default=None
    # )


# UNIVERSAL API MODELS (mimic OpenAI API)
class TextEmbeddingInput(BaseDocWithoutId):
    """The input to the API for text embedding. OpenAI compatible"""

    model: str = Field(
        description='The identifier of the model.\n'
        '\nAvailable models and corresponding param size and dimension:\n'
        '\nFor more information, please checkout our [technical blog](https://arxiv.org/abs/2307.11224).\n',  # noqa
    )

    input: Union[List[Optional[str]], Optional[str], List[TextDoc], TextDoc] = Field(
        description='List of texts to embed',
    )
    encoding_type: Optional[
        Union[
            Literal['float', 'base64', 'binary', 'ubinary'],
            List[Literal['float', 'base64', 'binary', 'ubinary']],
        ]
    ] = Field(
        description='The format in which you want the embeddings to be returned.'
        'Possible value are `float`, `base64`, `binary`, `ubinary` or a list '
        'containing any of them. Defaults to `float`',
        alias='embedding_type',
    )
    task_type: Optional[
        Literal['query', 'document', 'sts', 'classification', 'clustering']
    ] = Field(
        description='Used to convey intended downstream application to help the model produce better embeddings. Must be one of the following values:\n'  # noqa
        '- "query": Specifies the given text is a query in a search or retrieval setting.\n'  # noqa
        '- "document": Specifies the given text is a document in a search or retrieval setting.\n'  # noqa
        '- "sts": Specifies the given text is used for Semantic Textual Similarity (STS).\n'  # noqa
        '- "classification": Specifies that the embedding is used for classification.\n'
        '- "clustering": Specifies that the embedding is used for clustering.\n',
        default=None,
    )
    dimensions: Optional[Literal[32, 64, 128, 256, 512, 1024]] = Field(
        description='Used to specify output embedding size. If set, output embeddings will be truncated to the size specified.',  # noqa
        default=None,
    )
    strategy: Optional[Literal['fixed', 'semantic']] = Field(
        description='Strategy to be used when chunking. Defaults to fixed',
        default=None,
    )
    chunk_size: Optional[int] = Field(
        description='Chunk size to be used. Relevant when "strategy" is set to fixed. 256 by default',  # noqa
        default=None,
    )

    @classmethod
    def validate(
        cls,
        value,
    ):
        if 'input' not in value:
            raise ValueError('"input" field missing')
        if 'model' not in value:
            raise ValueError('you must provide a model parameter')

        return super().validate(value)

    class Config(BaseDoc.Config):
        extra = 'forbid'
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "model": "jina-embeddings-v3",
                "input": ["Hello, world!"],
            },
        }


class ChunkEmbeddingsObject(BaseDocWithoutId):
    """Embedding object. OpenAI compatible"""

    object: str = 'embeddings'
    index: int = Field(
        description='The index of the embedding output, corresponding to the index in the list of inputs'  # noqa
    )
    embeddings: Union[
        List[bytes], NdArray, Dict[str, Union[List[bytes], NdArray]]
    ] = Field(
        description='A tensor of embeddings for the text where each embedding '
        'correspond to a chunk. It may come as the base64 encoded of the embeddings '
        'tensor if "encoding_type" is "base64". It can be rebuilt in the client as '
        '`np.frombuffer(base64.b64decode(embeddings), dtype=np.float32)`. In case of '
        'multiple "encoding_type" are requested, they will be returned in a '
        'dictionary where the key is the encoding format.'
    )
    chunks: List[str] = Field(description='The chunks returned ')

    # truncated: Optional[bool] = Field(
    #     description='Flag to inform that the embedding is computed ', default=None
    # )

    class Config(BaseDocWithoutId.Config):
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "object": "embeddings",
                "index": 0,
                "embeddings": [[0.1, 0.2, 0.3], [0.5, 0.6, 0.7]],
            }
        }


class ChunkedModelEmbeddingsOutput(BaseInputModel):
    """Output of the embedding service"""

    object: str = 'list'
    data: DocList[ChunkEmbeddingsObject] = Field(
        description='A list of Embedding Objects returned by the embedding service'
    )
    usage: Usage = Field(
        description='Total usage of the request. Sums up the usage from each individual input'  # noqa
    )

    class Config(BaseInputModel.Config):
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "data": [
                    {
                        "index": 0,
                        "embeddings": [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]],
                        "object": "embeddings",
                    },
                    {
                        "index": 1,
                        "embeddings": [[0.6, 0.5, 0.4], [0.3, 0.2, 0.1]],
                        "object": "embeddings",
                    },
                ],
                "usage": {"total_tokens": 15},
            }
        }
