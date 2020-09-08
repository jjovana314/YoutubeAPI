import helper
from http import HTTPStatus


class Items:
    def __init__(self, kind: str, etag: str, id_: dict):
        self.kind = kind
        self.etag = etag
        self.id_ = id_

    @property
    def kind(self):
        return self._kind

    @kind.setter
    def kind(self, value):
        self._kind = value

    @property
    def etag(self):
        return self._etag

    @etag.setter
    def etag(self, value):
        self._etag = value

    @property
    def id_(self):
        return self._id

    @id_.setter
    def id_(self, value):
        self._id = value

    def get_id_values(self):
        return tuple(self._id.values())

    def get_id_keys(self):
        return tuple(self._id.keys())

    def id_validation(self):
        video_id = self.id_.get("videoId", None)
        channel_id = self.id_.get("channelId", None)

        if not (video_id is None) ^ (channel_id is None):
            raise ValueError("Please enter videoId or channelId", HTTPStatus.BAD_REQUEST)

    def __eq__(self, other):
        return (isinstance(other, Items) and
                self.kind == other.kind and
                self.etag == other.etag and
                self.id_ == other.id_)

    def __hash__(self):
        return hash((self.kind, self.etag, self.id_))

    def __repr__(self):
        return f"{__class__.__name__}(kind={self.kind}, etag={self.etag}, id_={self.id_})"

    def __str__(self):
        return f"({self.kind}, {self.etag}, {self.id_})"