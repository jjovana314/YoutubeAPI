import helper
from http import HTTPStatus


class Data:
    """ Outter data class. """
    def __init__(
        self, kind: str, etag: str, next_page_token: str, region_code: str, page_info: dict
    ):
        """
        Args:
            kind (str): what kind of data is recieved (response or request)
            etag (str): determine if a resource is changed
            next_page_token (str): token of next page
            region_code (str): force API to show data only in specific country
            page_info (dict): information about current page
                              (total results, results per page)
        """
        self.kind = kind
        self.etag = etag
        self.next_page_token = next_page_token
        self.region_code = region_code
        self.page_info = page_info

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
    def next_page_token(self) -> str:
        return self._next_page_token

    @next_page_token.setter
    def next_page_token(self, value: str) -> None:
        self._next_page_token = value

    @property
    def region_code(self) -> str:
        return self._region_code

    @region_code.setter
    def region_code(self, value: str) -> None:
        self._region_code = value

    @property
    def page_info(self) -> dict:
        return self._page_info

    @page_info.setter
    def page_info(self, value) -> None:
        self._page_info_validation(value)

    def _page_info_validation(self, value: dict) -> None:
        """ Validate and set self._page_info.

        Args:
            value (dict): data for validation

        Raises:
            ValueError: if total_results is less than results_per_page
        """
        total_results = value["totalResults"]
        results_per_page = value["resultsPerPage"]
        if total_results < results_per_page:
            raise ValueError(
                "Total results cannot be less than results per page",
                HTTPStatus.BAD_REQUEST
            )
        else:
            setattr(self._page_info, value)

    def get_page_info_values(self) -> tuple:
        """ Returns tuple of values from page_info dictionary. """
        return tuple(self.page_info.values())

    def get_page_info_keys(self) -> tuple:
        """ Returns tuple of keys from page_info dictionary. """
        return tuple(self.page_info.keys())

    def __eq__(self, other: Data) -> bool:
        return (isinstance(other, Data) and
                self.kind == other.kind and
                self.etag == other.etag and
                self.next_page_token == other.next_page_token and
                self.region_code == other.region_code and
                self.page_info == other.page_info)

    def __repr__(self) -> str:
        return (f"{__class__.__name__}(kind={self.kind}, ",
                f"etag={self.etag}, next_page_token={self.next_page_token}, "
                f"region_code={self.region_code}, page_info={self.page_info})")

    def __str__(self) -> str:
        return (f"({self.kind}, {self.etag}, {self.next_page_token}, "
                f"{self.region_code}, {self.page_info})")

    def __hash__(self) -> int:
        return hash((self.kind,
                     self.etag,
                     self.next_page_token,
                     self.region_code,
                     self.page_info))
