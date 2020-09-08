import helper
from http import HTTPStatus


class Items:
    """ Class for validating items data. """
    def __init__(self, kind: str, etag: str, id_: dict):
        """
        Args:
            kind (str): what kind of API we currently have
            etag (str): determine if resource is changed
            id_ (dict): dictionary with kind and channel_id or video_id keys
                        that give us details about research data,
                        for example, tell us that result is channel or video

        Note:
            item can be only video or channel
        """
        self.kind = kind
        self.etag = etag
        self.id_ = id_

    @property
    def kind(self) -> str:
        return self._kind

    @kind.setter
    def kind(self, value: str) -> None:
        self._kind = value

    @property
    def etag(self) -> str:
        return self._etag

    @etag.setter
    def etag(self, value: str) -> None:
        self._etag = value

    @property
    def id_(self) -> dict:
        return self._id

    @id_.setter
    def id_(self, value: dict) -> None:
        self._id_validation(value)

    def get_id_values(self) -> tuple:
        return tuple(self._id.values())

    def get_id_keys(self) -> tuple:
        return tuple(self._id.keys())

    def _id_validation(self, value: dict) -> None:
        video_id = value.get("videoId", None)
        channel_id = value.get("channelId", None)

        if not (video_id is None) ^ (channel_id is None):
            raise ValueError("Please enter videoId or channelId", HTTPStatus.BAD_REQUEST)
        else:
            setattr(self._id, value)

    def __eq__(self, other: Items) -> bool:
        return (isinstance(other, Items) and
                self.kind == other.kind and
                self.etag == other.etag and
                self.id_ == other.id_)

    def __hash__(self) -> int:
        return hash((self.kind, self.etag, self.id_))

    def __repr__(self) -> str:
        return f"{__class__.__name__}(kind={self.kind}, etag={self.etag}, id_={self.id_})"

    def __str__(self) -> str:
        return f"({self.kind}, {self.etag}, {self.id_})"