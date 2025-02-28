from abc import ABC, abstractmethod
from enum import StrEnum
from typing import Annotated, Any, Literal, Optional, Type, TypeVar

from pydantic import BaseModel, Field

from ormy.base.generic import TabularData
from ormy.base.pydantic import BaseReference, TableResponse

# ----------------------- #


class SortOrder(StrEnum):
    """
    Sort Order Enum

    Attributes:
        asc (str): Ascending Order
        desc (str): Descending Order
    """

    asc = "asc"
    desc = "desc"


# ....................... #


class SortField(BaseModel):
    """
    Sort field model

    Attributes:
        key (str): Key of the field
        title (str): The field title
        default (bool): Whether the Field is the default sort field
    """

    key: str
    # title: str  # TODO: remove title
    default: bool = False


# ----------------------- #
# TODO: add filter operators (mb use a separate uniform interface)

F = TypeVar("F", bound="FilterABC")


class FilterABC(ABC, BaseModel):
    """
    Abstract Base Class for Search Filters

    Attributes:
        key (str): Key of the filter
        value (Any, optional): The filter value
        type (str): The filter type
    """

    key: str
    # title: Optional[str] = None  # TODO: remove title
    value: Optional[Any] = None
    type: str = "abc"

    # ....................... #

    @abstractmethod
    def build(self) -> Optional[str]: ...


# ....................... #


class BooleanFilter(FilterABC):
    """
    Boolean Filter Model

    Attributes:
        key (str): Key of the filter
        value (bool): The filter value
    """

    value: Optional[bool] = None
    type: Literal["boolean"] = "boolean"

    # ....................... #

    def build(self):
        if self.value is not None:
            return f"{self.key} = {str(self.value).lower()}"

        return None


# ....................... #


class NumberFilter(FilterABC):
    """
    Number Filter Model

    Attributes:
        key (str): Key of the filter
        value (Tuple[float | None, float | None]): The filter value
    """

    value: tuple[Optional[float], Optional[float]] = (None, None)
    type: Literal["number"] = "number"

    # ....................... #

    def build(self):
        low, high = self.value

        if low is None and high is not None:
            return f"{self.key} <= {high}"

        if low is not None and high is None:
            return f"{self.key} >= {low}"

        if low is not None and high is not None:
            return f"{self.key} {low} TO {high}"

        return None


# ....................... #


class DatetimeFilter(FilterABC):
    """
    Datetime Filter Model

    Attributes:
        key (str): Key of the filter
        value (Tuple[int | None, int | None]): The filter value
    """

    value: tuple[Optional[int], Optional[int]] = (None, None)
    type: Literal["datetime"] = "datetime"

    # ....................... #

    def build(self):
        low, high = self.value

        if low is None and high is not None:
            return f"{self.key} <= {high}"

        if low is not None and high is None:
            return f"{self.key} >= {low}"

        if low is not None and high is not None:
            return f"{self.key} {low} TO {high}"

        return None


# ....................... #


class ArrayFilter(FilterABC):
    """
    Array Filter Model

    Attributes:
        key (str): Key of the filter
        value (list[Any]): The filter value
    """

    value: list[Any] = []
    type: Literal["array"] = "array"

    # ....................... #

    def build(self):
        if self.value:
            return f"{self.key} IN {self.value}"

        return None


# ....................... #

AnyFilter = Annotated[
    BooleanFilter | NumberFilter | DatetimeFilter | ArrayFilter,
    Field(discriminator="type"),
]

# ----------------------- #


class SearchRequest(BaseModel):
    query: str = ""
    sort: Optional[str] = None
    order: SortOrder = SortOrder.desc
    filters: list[AnyFilter] = []


# ----------------------- #

S = TypeVar("S", bound="SearchResponse")


class SearchResponse(TableResponse):
    @classmethod
    def from_search_results(
        cls: Type[S],
        res: Any,
    ) -> S:
        """
        ...
        """

        # TODO: Replace with ormy errors

        assert res.hits is not None, "Hits must be provided"
        assert res.hits_per_page is not None, "Hits per page must be provided"
        assert res.page is not None, "Page must be provided"
        assert res.total_hits is not None, "Total hits must be provided"

        return cls(
            hits=TabularData(res.hits),
            size=res.hits_per_page,
            page=res.page,
            count=res.total_hits,
        )


# ....................... #


class MeilisearchReference(BaseReference):
    sort: list[SortField] = []
    filters: list[AnyFilter] = []


# ....................... #


class MeilisearchReferenceV2(BaseModel):
    """
    Meilisearch Reference V2 model

    Attributes:
        sort (list[ormy.extension.meilisearch.schema.SortField]): The sort fields
        filters (list[ormy.extension.meilisearch.schema.AnyFilter]): The filters
    """

    sort: list[SortField] = []
    filters: list[AnyFilter] = []
