import helper


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
        # helper.validate_type(value, str)
        self._kind = value

    @property
    def etag(self):
        return self._etag

    @etag.setter
    def etag(self, value):
        # helper.validate_type(value, str)
        self._etag = value

    @property
    def id_(self):
        return self._id

    @id_.setter
    def id_(self, value):
        # helper.validate_type(value, dict)
        self._id = value
        