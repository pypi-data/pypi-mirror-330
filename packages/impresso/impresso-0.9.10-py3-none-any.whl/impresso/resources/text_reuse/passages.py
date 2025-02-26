from pandas import DataFrame, json_normalize

from impresso.api_client.api.search_facets import get_tr_passages_facet
from impresso.api_client.api.text_reuse_passages import find_text_reuse_passages
from impresso.api_client.models.find_text_reuse_passages_order_by import (
    FindTextReusePassagesOrderBy,
    FindTextReusePassagesOrderByLiteral,
)
from impresso.api_client.models.get_tr_passages_facet_id import (
    GetTrPassagesFacetId,
    GetTrPassagesFacetIdLiteral,
)
from impresso.api_client.models.get_tr_passages_facet_order_by import (
    GetTrPassagesFacetOrderBy,
)
from impresso.api_client.types import UNSET, Unset
from impresso.api_models import (
    BaseFind,
    SearchFacetBucket,
    TextReusePassage,
)
from impresso.data_container import DataContainer
from impresso.resources.base import Resource
from impresso.resources.search import FacetDataContainer
from impresso.resources.text_reuse.clusters import Range, _build_filters
from impresso.structures import AND, OR, DateRange
from impresso.util.error import raise_for_error
from impresso.util.filters import and_or_filter, filters_as_protobuf
from impresso.util.py import get_enum_from_literal


class FindTextReusePassageResponseSchema(BaseFind):
    """Schema for the text reuse passage response."""

    data: list[TextReusePassage]


class FindTextReusePassagesContainer(DataContainer):
    """Response of a find text reuse passages call."""

    @property
    def df(self) -> DataFrame:
        """Return the data as a pandas dataframe."""
        data = self._data.to_dict()["data"]
        if len(data):
            return json_normalize(self._data.to_dict()["data"]).set_index("uid")
        return DataFrame()


class TextReusePassagesResource(Resource):
    """Text reuse passages resource."""

    name = "textReusePassages"

    def find(
        self,
        term: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        order_by: FindTextReusePassagesOrderByLiteral | None = None,
        cluster_id: str | AND[str] | OR[str] | None = None,
        cluster_size: Range | AND[Range] | OR[Range] | None = None,
        title: str | AND[str] | OR[str] | None = None,
        lexical_overlap: Range | AND[Range] | OR[Range] | None = None,
        day_delta: Range | AND[Range] | OR[Range] | None = None,
        date_range: DateRange | None = None,
        newspaper_id: str | OR[str] | None = None,
        collection_id: str | OR[str] | None = None,
        front_page: bool | None = None,
        topic_id: str | AND[str] | OR[str] | None = None,
        language: str | OR[str] | None = None,
        country: str | OR[str] | None = None,
        mention: str | AND[str] | OR[str] | None = None,
        entity_id: str | AND[str] | OR[str] | None = None,
    ) -> FindTextReusePassagesContainer:
        # reusing build filters from clusters - they are the same
        filters = _build_filters(
            cluster_id=cluster_id,
            cluster_size=cluster_size,
            title=title,
            lexical_overlap=lexical_overlap,
            day_delta=day_delta,
            date_range=date_range,
            newspaper_id=newspaper_id,
            collection_id=collection_id,
            front_page=front_page,
            topic_id=topic_id,
            language=language,
            country=country,
            mention=mention,
            entity_id=entity_id,
        )
        if term is not None:
            filters.extend(and_or_filter(term, "string"))
        filters_pb = filters_as_protobuf(filters or [])

        result = find_text_reuse_passages.sync(
            client=self._api_client,
            limit=limit if limit is not None else UNSET,
            offset=offset if offset is not None else UNSET,
            order_by=(
                get_enum_from_literal(order_by, FindTextReusePassagesOrderBy)
                if order_by is not None
                else UNSET
            ),
            filters=filters_pb if filters_pb else UNSET,
        )
        raise_for_error(result)
        return FindTextReusePassagesContainer(
            result,
            FindTextReusePassageResponseSchema,
            web_app_search_result_url=_build_web_app_find_passages_url(
                base_url=self._get_web_app_base_url(),
                filters=filters_pb,
                limit=limit,
                offset=offset,
                order_by=order_by,
            ),
        )

    def facet(
        self,
        facet: GetTrPassagesFacetIdLiteral,
        term: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        order_by: FindTextReusePassagesOrderByLiteral | None = None,
        cluster_id: str | AND[str] | OR[str] | None = None,
        cluster_size: Range | AND[Range] | OR[Range] | None = None,
        title: str | AND[str] | OR[str] | None = None,
        lexical_overlap: Range | AND[Range] | OR[Range] | None = None,
        day_delta: Range | AND[Range] | OR[Range] | None = None,
        date_range: DateRange | None = None,
        newspaper_id: str | OR[str] | None = None,
        collection_id: str | OR[str] | None = None,
        front_page: bool | None = None,
        topic_id: str | AND[str] | OR[str] | None = None,
        language: str | OR[str] | None = None,
        country: str | OR[str] | None = None,
        mention: str | AND[str] | OR[str] | None = None,
        entity_id: str | AND[str] | OR[str] | None = None,
    ) -> FacetDataContainer:
        facet_id = get_enum_from_literal(facet, GetTrPassagesFacetId)
        if isinstance(facet_id, Unset):
            raise ValueError(f"{facet} is not a valid value")

        filters = _build_filters(
            cluster_id=cluster_id,
            cluster_size=cluster_size,
            title=title,
            lexical_overlap=lexical_overlap,
            day_delta=day_delta,
            date_range=date_range,
            newspaper_id=newspaper_id,
            collection_id=collection_id,
            front_page=front_page,
            topic_id=topic_id,
            language=language,
            country=country,
            mention=mention,
            entity_id=entity_id,
        )

        if term is not None:
            filters.extend(and_or_filter(term, "string"))

        filters_pb = filters_as_protobuf(filters or [])

        result = get_tr_passages_facet.sync(
            client=self._api_client,
            id=facet_id,
            filters=filters_pb if filters_pb else UNSET,
            offset=offset if offset is not None else UNSET,
            limit=limit if limit is not None else UNSET,
            order_by=(
                get_enum_from_literal(order_by, GetTrPassagesFacetOrderBy)
                if order_by is not None
                else get_enum_from_literal("value", GetTrPassagesFacetOrderBy)
            ),
        )
        raise_for_error(result)
        return FacetDataContainer(
            result,
            SearchFacetBucket,
            web_app_search_result_url=_build_web_app_find_passages_url(
                base_url=self._get_web_app_base_url(),
                filters=filters_pb,
                limit=limit,
                offset=offset,
                order_by=order_by,
            ),
        )


def _build_web_app_find_passages_url(
    base_url: str,
    filters=str | None,
    limit=int | None,
    offset=int | None,
    order_by=FindTextReusePassagesOrderBy | None,
) -> str:
    page = offset // limit if limit is not None and offset is not None else 0
    query_params = {
        "sort": order_by,
        "sq": filters,
        "p": page + 1,
    }
    query_string = "&".join(
        f"{key}={value}" for key, value in query_params.items() if value is not None
    )
    url = f"{base_url}/text-reuse/passages"
    return f"{url}?{query_string}" if query_string else url
