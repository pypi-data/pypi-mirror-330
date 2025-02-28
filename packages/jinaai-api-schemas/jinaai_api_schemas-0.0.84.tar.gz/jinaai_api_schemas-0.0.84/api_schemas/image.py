from typing import Optional, Union

from docarray import BaseDoc
from docarray.base_doc.doc import BaseDocWithoutId
from docarray.typing.bytes import ImageBytes
from docarray.typing.url import AnyUrl
from docarray.utils._internal.pydantic import bytes_validator
from pydantic import Field, root_validator


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


class ImageDocWithoutId(BaseDocWithoutId):
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


class TextOrImageDoc(BaseDoc):
    text: Optional[str] = None
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
            value.get('text', None) is None
            and value.get('image', None) is None
            and value.get('url', None) is None
            and value.get('bytes', None) is None
        ):
            raise ValueError('text, image, URL or bytes need to be provided')
        if value.get('text', None) is not None and (
            value.get('image', None) is not None
            or value.get('url', None) is not None
            or value.get('bytes', None) is not None
        ):
            raise ValueError('text or image cannot be provided in the same input')
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
