import helper


class Data:
    def __init__(
        self, kind: str, etag: str, next_page_token: str, region_code: str, page_info: dict
    ):
        self.kind = kind
        self.etag = etag
        self.next_page_token = next_page_token
        self.region_code = region_code
        self.page_info = page_info

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
    def next_page_token(self):
        return self._next_page_token

    @next_page_token.setter
    def next_page_token(self, value):
        # helper.validate_type(value, str)
        self._next_page_token = value

    @property
    def region_code(self):
        return self._region_code

    @region_code.setter
    def region_code(self, value):
        # helper.validate_type(value, str)
        self._region_code = value

    @property
    def page_info(self):
        return self._page_info

    @page_info.setter
    def page_info(self, value):
        # helper.validate_type(value, dict)
        self._page_info = value
