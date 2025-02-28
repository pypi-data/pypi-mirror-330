from typing import Dict, List, Optional, Union

from docarray import BaseDoc, DocList
from docarray.base_doc.doc import BaseDocWithoutId
from docarray.typing import NdArray
from docarray.typing.bytes import ImageBytes
from docarray.typing.url import AnyUrl
from docarray.utils._internal.pydantic import bytes_validator
from pydantic import BaseModel, Field, root_validator


class ExecutorUsage(BaseDoc):
    """The usage of the embedding services to report, e.g. number of tokens in case of text input"""  # noqa

    total_tokens: int = Field(
        description='The number of tokens used to embed the input text'
    )


# EXECUTOR MODELS
## Model to be imported by the Executor and used by the Universal API
class TextDoc(BaseDoc):
    """Document containing a text field"""

    text: str


class SerializeImageBytes(ImageBytes):
    @classmethod
    def _docarray_validate(
        cls,
        value,
    ):
        if isinstance(value, str):
            import base64

            return cls(base64.b64decode(value))
        else:
            value = bytes_validator(value)
            return cls(value)

    def _docarray_to_json_compatible(self):
        """
        Convert itself into a json compatible object
        """
        import base64

        encoded_str = base64.b64encode(self).decode('utf-8')
        return encoded_str


class Url(AnyUrl):
    @classmethod
    def _docarray_validate(
        cls,
        value,
    ):
        import urllib.parse

        if isinstance(value, str):
            if urllib.parse.urlparse(value).scheme not in {'http', 'https'}:
                raise ValueError(
                    'This does not have a valid URL schema ("http" or "https")'
                )

        return cls(value)

    @classmethod
    def is_extension_allowed(cls, value) -> bool:
        """Returns a list of allowed file extensions for the class
        that are not covered by the mimetypes library."""
        import urllib.parse

        if isinstance(value, str):
            if urllib.parse.urlparse(value).scheme in {'http', 'https'}:
                return True
            else:
                return False

        return True


class ImageDoc(BaseDoc):
    """ImageDoc with fields"""

    url: Optional[Url] = Field(
        description='URL of an image file',
        default=None,
    )
    bytes: Optional[SerializeImageBytes] = Field(
        description='base64 representation of the Image.',
        default=None,
    )
    image: Optional[Union[Url, SerializeImageBytes]] = Field(
        description='Image representation that can hold URL of an image or a base64 representation',  # noqa
        default=None,
    )

    @root_validator(pre=False)
    def validate_all_input(cls, value):
        if (
            value.get('image', None) is None
            and value.get('url', None) is None
            and value.get('bytes', None) is None
        ):
            raise ValueError('image, URL or bytes need to be provided')
        if value.get('image', None) is not None:
            image = value.get('image')
            if isinstance(image, SerializeImageBytes):
                value['bytes'] = image
                value['image'] = None
            elif isinstance(image, AnyUrl):
                value['url'] = image
                value['image'] = None
            else:
                raise ValueError(
                    'image must be a valid URL or base64 image representation'
                )
        return value

    @classmethod
    def validate(
        cls,
        value,
    ):
        if 'image' not in value and 'url' not in value and 'bytes' not in value:
            raise ValueError('image, URL or bytes need to be provided')
        return super().validate(value)


class ClassificationInput(BaseDocWithoutId):
    """The input to the API for classify endpoint. OpenAI compatible"""

    model: Optional[str] = Field(
        description='The identifier of the model.\n'
        '\nAvailable models and corresponding param size and dimension:\n'
        '- `jina-clip-v1`,\t223M,\t768\n'
        '- `jina-clip-v2`,\t865M,\t1024\n'
        '- `jina-embeddings-v2-base-en`,\t137M,\t768\n'
        '- `jina-embeddings-v2-base-es`,\t161M,\t768\n'
        '- `jina-embeddings-v2-base-de`,\t161M,\t768\n'
        '- `jina-embeddings-v2-base-zh`,\t161M,\t768\n'
        '- `jina-embeddings-v2-base-code`,\t137M,\t768\n'
        '- `jina-embeddings-v3`,\t570M,\t1024\n'
        '\nFor more information, please checkout our [technical blog](https://arxiv.org/abs/2307.11224).\n',  # noqa
    )
    classifier_id: Optional[str] = Field(
        description='The identifier of the classifier. '
        'If not provided, a new classifier will be created.'
        '\nYou can provide only either `model` or `classifier_id`',
    )
    input: Union[List[Union[TextDoc, ImageDoc, str]], TextDoc, ImageDoc, str] = Field(
        description='List of text and images or a single text and image for classification',  # noqa
    )
    labels: Optional[Union[List[str], Dict[str, List[str]]]] = Field(
        description='List of labels or a dictionary of structured labels for zero-shot classification',  # noqa
    )

    @classmethod
    def validate(
        cls,
        value,
    ):
        if 'classifier_id' not in value and 'model' not in value:
            raise ValueError(
                'For zero-shot classification, you must provide a "model" parameter, for few-shot classification, you must provide a "classifier_id" parameter'  # noqa
            )
        if 'classifier_id' in value and 'model' in value:
            raise ValueError('You can provide only either "model" or "classifier_id"')
        if 'input' not in value:
            raise ValueError('"input" field missing')
        if 'model' in value and 'labels' not in value:
            raise ValueError('"labels" field missing')
        if 'classifier_id' in value and 'labels' in value:
            raise ValueError(
                '"labels" field should not be provided for few-shot classification'
            )
        return super().validate(value)

    class Config(BaseDoc.Config):
        extra = 'forbid'
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "model": "jina-embeddings-v3",
                "input": [
                    {"text": "text1"},
                    {"text": "text2"},
                    {"text": "text3"},
                ],
                "labels": ["label1", "label2", "label3"],
            }
        }


class ClassificationLabelScore(BaseDocWithoutId):
    label: str = Field(description='The label of the classification output')
    score: float = Field(
        description='The confidence score of the classification output'
    )


class ClassificationObject(BaseDocWithoutId):
    """Classification object"""

    object: str = 'classification'
    index: int = Field(
        description='The index of the classification output, corresponding to the index in the list of inputs'  # noqa
    )
    prediction: Union[str, Dict[str, str]] = Field(
        description='The label with the highest probability'
    )
    score: Union[float, Dict[str, float]] = Field(
        description='The confidence score of the classification output'
    )
    predictions: Union[
        List[ClassificationLabelScore], Dict[str, List[ClassificationLabelScore]]
    ] = Field(description='List of labels and their scores')

    class Config(BaseDocWithoutId.Config):
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "object": "classification",
                "prediction": "label1",
                "score": 0.75,
                "predictions": [
                    {"label": "label1", "score": 0.75},
                    {"label": "label2", "score": 0.25},
                ],
            }
        }


class Usage(BaseModel):
    total_tokens: int = Field(
        description='The number of tokens used by all the texts in the input'
    )


class ClassificationOutput(BaseDocWithoutId):
    """Output of the classification service"""

    data: DocList[ClassificationObject] = Field(
        description='A list of Classification Objects returned by the classification service'  # noqa
    )
    usage: Usage = Field(
        description='Total usage of the request. Sums up the usage from each individual input'  # noqa
    )

    class Config(BaseDocWithoutId.Config):
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "data": [
                    {
                        "index": 0,
                        "prediction": "label1",
                        "object": "classification",
                        "score": 0.75,
                        "predictions": [
                            {"label": "label1", "score": 0.75},
                            {"label": "label2", "score": 0.25},
                        ],
                    },
                    {
                        "index": 1,
                        "prediction": "label2",
                        "object": "classification",
                        "score": 0.54,
                        "predictions": [
                            {"label": "label2", "score": 0.54},
                            {"label": "label1", "score": 0.46},
                        ],
                    },
                ],
                "usage": {"total_tokens": 15},
            }
        }


class ExecutorClassificationInputDoc(BaseDoc):
    embedding: NdArray = Field(description='The embedding of the input', default=[])


class ExecutorClassificationOutputDoc(BaseDoc):
    prediction: Union[str] = Field(description='The label with the highest probability')
    score: float = Field(
        description='The confidence score of the classification output'
    )
    predictions: List[ClassificationLabelScore] = Field(
        description='List of labels and their scores'
    )
    usage: ExecutorUsage = Field(description='Total usage of the request')
