from typing import List, Literal, Optional, Union

from docarray import BaseDoc
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


class TextExampleDoc(BaseDoc):
    """Document containing a text field and a label"""

    text: str = Field(description='The example text')
    label: Union[str] = Field(description='The label of the text')

    @classmethod
    def validate(
        cls,
        value,
    ):
        if 'text' not in value and 'label' not in value:
            raise ValueError('"text" and "label" fields missing')
        elif 'text' not in value:
            raise ValueError('"text" field missing')
        elif 'label' not in value:
            raise ValueError('"label" field missing')
        return super().validate(value)


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


class ImageExampleDoc(BaseDoc):
    """ImageDoc with fields and a label"""

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
    label: Union[str] = Field(description='The label of the image')

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
        if (
            'image' not in value
            and 'url' not in value
            and 'bytes' not in value
            and 'label' not in value
        ):
            raise ValueError('image, URL or bytes and label need to be provided')
        elif 'image' not in value and 'url' not in value and 'bytes' not in value:
            raise ValueError('image, URL or bytes need to be provided')
        elif 'label' not in value:
            raise ValueError('"label" field missing')
        return super().validate(value)


class TrainingInput(BaseDocWithoutId):
    """The input to the API for train the classifier. OpenAI compatible"""

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
        '\nFor more information, please checkout our [technical blog](https://arxiv.org/abs/2307.11224).\n'  # noqa
        '\nYou can provide only either `model` or `classifier_id`',
    )
    classifier_id: Optional[str] = Field(
        description='The identifier of the classifier. '
        'If not provided, a new classifier will be created.'
        '\nYou can provide only either `model` or `classifier_id`',
    )
    access: Literal['public', 'private'] = Field(
        description='The accessibility of the classifier when created. '
        'Will be ignored if `classifier_id` is provided',
        default='private',
    )
    input: Union[
        List[Union[TextExampleDoc, ImageExampleDoc]], TextExampleDoc, ImageExampleDoc
    ] = Field(
        description='List of text and images and labels or a single text and image and label to train the classifier',  # noqa
    )
    num_iters: Optional[int] = Field(
        description='The number of iterations to train the classifier', default=10
    )

    @classmethod
    def validate(
        cls,
        value,
    ):
        if 'input' not in value:
            raise ValueError('"input" field missing')
        if 'model' not in value and 'classifier_id' not in value:
            raise ValueError('"model" or "classifier_id" field missing')
        if 'model' in value and 'classifier_id' in value:
            raise ValueError(
                'only either "model" or "classifier_id" should be provided'
            )
        return super().validate(value)

    class Config(BaseDoc.Config):
        extra = 'forbid'
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "model": "jina-embeddings-v3",
                "access": "private",
                "input": [
                    {"text": "text1", "label": "label1"},
                    {"text": "text2", "label": "label2"},
                    {"text": "text3", "label": "label3"},
                ],
                "num_iters": 10,
            },
        }


class Usage(BaseModel):
    total_tokens: int = Field(
        description='The number of tokens used by all the texts in the input'
    )


class TrainingOutput(BaseDocWithoutId):
    """Output of the training service"""

    classifier_id: str = Field(
        description='The identifier of the classifier that was trained'
    )
    num_samples: int = Field(
        description='The number of samples that were used to train the classifier'
    )
    usage: Usage = Field(
        description='Total usage of the request. Sums up the usage from each individual input'  # noqa
    )

    class Config(BaseDocWithoutId.Config):
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "classifier_id": "classifier_id",
                "num_samples": 10,
                "usage": {"total_tokens": 15},
            }
        }


class ClassifierParameters(BaseModel):
    model_name: str = Field(description='The model name')
    weights: Optional[List[List[float]]] = Field(
        description='The weights of the classifier', default=None
    )
    bias: Optional[List[float]] = Field(
        description='The bias of the classifier', default=None
    )
    iteration_count: Optional[int] = Field(
        description='The number of iterations', default=None
    )
    labels: Optional[list] = Field(
        description='The labels of the classifier', default=None
    )

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "model_name": "model_name",
                "weights": [[1, 2], [3, 4], [5, 6]],
                "bias": [1, 2],
                "iteration_count": 100,
                "labels": ["label1", "label2", "label3"],
            }
        }


class ExecutorTrainingInputParameters(ClassifierParameters):
    num_iters: Optional[int] = Field(
        description='The number of iterations to train the classifier', default=10
    )


class ExecutorTrainingInputDoc(BaseDoc):
    embedding: NdArray = Field(description='The embedding of the input', default=[])
    label: Optional[str] = Field(description='The label of the input', default=None)


class ExecutorTrainingOutputDoc(BaseDoc, ClassifierParameters):
    usage: ExecutorUsage = Field(description='The usage of the request')
