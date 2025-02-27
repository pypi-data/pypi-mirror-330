from typing import Optional

from ..core import Object


class Document(Object):
    def __init__(
        self,
        id=None,
        type="Document",
        content=None,
        url=None,
        sensitive: Optional[bool] = None,
        **kwargs,
    ):
        super().__init__(id=id, type=type, content=content, **kwargs)
        self.url = url
        self.sensitive = sensitive

    def to_dict(self, _extras: Optional[dict] = None):
        data = super().to_dict()

        if self.url:
            data["url"] = self.url

        return data


class Page(Document):
    def __init__(self, **kwargs):
        kwargs["type"] = "Page"
        super().__init__(**kwargs)


class Audio(Document):
    def __init__(self, **kwargs):
        kwargs["type"] = "Audio"
        super().__init__(**kwargs)


class Image(Document):
    def __init__(self, **kwargs):
        kwargs["type"] = "Image"
        super().__init__(**kwargs)


class Video(Document):
    def __init__(self, **kwargs):
        kwargs["type"] = "Video"
        super().__init__(**kwargs)
