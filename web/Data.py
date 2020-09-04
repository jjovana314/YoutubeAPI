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
        self._kind = value

    @property
    def etag(self):
        return self._etag

    @etag.setter
    def etag(self, value):
        self._etag = value

    @property
    def next_page_token(self):
        return self._next_page_token

    @next_page_token.setter
    def next_page_token(self, value):
        self._next_page_token = value

    @property
    def region_code(self):
        return self._region_code

    @region_code.setter
    def region_code(self, value):
        self._region_code = value

    @property
    def page_info(self):
        return self._page_info

    @page_info.setter
    def page_info(self, value):
        self._page_info = value

    def page_info_validation(self):
        total_results = self.page_info["totalResults"]
        results_per_page = self.page_info["resultsPerPage"]
        if total_results < results_per_page:
            raise ValueError(
                "Total results cannot be less than results per page"
            )

    def get_page_info_values(self):
        return tuple(self.page_info.values())

    def get_page_info_keys(self):
        return tuple(self.page_info.keys())

    def __eq__(self, other):
        return (isinstance(other, Data) and
                self.kind == other.kind and
                self.etag == other.etag and
                self.next_page_token == other.next_page_token and
                self.region_code == other.region_code and
                self.page_info == other.page_info)

    def __repr__(self):
        return (f"{__class__.__name__}(kind={self.kind}, ",
                f"etag={self.etag}, next_page_token={self.next_page_token}, "
                f"region_code={self.region_code}, page_info={self.page_info})")

    def __str__(self):
        return (f"({self.kind}, {self.etag}, {self.next_page_token}, "
                f"{self.region_code}, {self.page_info})")

    def __hash__(self):
        return hash((self.kind,
                     self.etag,
                     self.next_page_token,
                     self.region_code,
                     self.page_info))
