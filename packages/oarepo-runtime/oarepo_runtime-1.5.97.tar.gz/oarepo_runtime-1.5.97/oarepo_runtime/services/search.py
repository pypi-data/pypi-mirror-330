import dataclasses
import inspect
from typing import List

from invenio_rdm_records.services.config import (
    RDMSearchDraftsOptions as BaseRDMSearchDraftsOptions,
)
from invenio_rdm_records.services.config import RDMSearchOptions as BaseRDMSearchOptions
from invenio_records_resources.proxies import current_service_registry
from invenio_records_resources.services.records import (
    SearchOptions as InvenioSearchOptions,
)
from invenio_records_resources.services.records.params import (
    FacetsParam,
    PaginationParam,
    QueryStrParam,
    SortParam,
)
from invenio_records_resources.services.records.queryparser import SuggestQueryParser
from invenio_search.engine import dsl

# TODO: integrate this to invenio_records_resources.services.records and remove SearchOptions class
from oarepo_runtime.i18n import lazy_gettext as _
from oarepo_runtime.records.systemfields.icu import ICUSuggestField
from oarepo_runtime.utils.functools import class_property

from .facets.params import GroupedFacetsParam

try:
    from invenio_i18n import get_locale
except ImportError:
    from invenio_i18n.babel import get_locale


class FuzzySuggestQueryParser(SuggestQueryParser):
    def __init__(self, identity=None, extra_params=None, **kwargs):
        """Constructor."""
        super().__init__(identity=identity, extra_params=extra_params)
        self.fields = self.extra_params.get("fields", [])
        self.extra_params.setdefault("type", "bool_prefix")

    def parse(self, query_str):
        """Parse the query."""
        # default behavior
        multi_match_with_bool_prefix = dsl.Q(
            "multi_match", query=query_str, **self.extra_params
        )
        # fuzziness does not seem to work with bool_prefix multimatch query, so we turn this into
        # should multi match query with two clauses
        multi_match_fuzzy = dsl.Q(
            "multi_match", query=query_str, fields=self.fields, fuzziness="AUTO"
        )
        return dsl.Q("bool", should=[multi_match_with_bool_prefix, multi_match_fuzzy])


class SearchOptionsMixin:
    @class_property
    def params_interpreters_cls(cls):
        """Replaces FacetsParam with GroupedFacetsParam."""
        param_interpreters = [*super(SearchOptionsMixin, cls).params_interpreters_cls]
        # replace FacetsParam with GroupedFacetsParam
        for idx, interpreter in enumerate(param_interpreters):
            if interpreter == FacetsParam:
                param_interpreters[idx] = GroupedFacetsParam
        return param_interpreters

    sort_options = {
        "title": dict(
            title=_("By Title"),
            fields=["metadata.title"],  # ES defaults to desc on `_score` field
        ),
        "bestmatch": dict(
            title=_("Best match"),
            fields=["_score"],  # ES defaults to desc on `_score` field
        ),
        "newest": dict(
            title=_("Newest"),
            fields=["-created"],
        ),
        "oldest": dict(
            title=_("Oldest"),
            fields=["created"],
        ),
    }


class SearchOptionsDraftMixin(SearchOptionsMixin):
    sort_options = {
        "bestmatch": dict(
            title=_("Best match"),
            fields=["_score"],  # search defaults to desc on `_score` field
        ),
        "updated-desc": dict(
            title=_("Recently updated"),
            fields=["-updated"],
        ),
        "updated-asc": dict(
            title=_("Least recently updated"),
            fields=["updated"],
        ),
        "newest": dict(
            title=_("Newest"),
            fields=["-created"],
        ),
        "oldest": dict(
            title=_("Oldest"),
            fields=["created"],
        ),
        "version": dict(
            title=_("Version"),
            fields=["-versions.index"],
        ),
    }


class SearchOptions(SearchOptionsMixin, InvenioSearchOptions):
    # TODO: should be changed
    params_interpreters_cls = [
        QueryStrParam,
        PaginationParam,
        SortParam,
        GroupedFacetsParam,
    ]


class RDMSearchOptions(SearchOptionsMixin, BaseRDMSearchOptions):
    pass


class RDMSearchDraftsOptions(SearchOptionsDraftMixin, BaseRDMSearchDraftsOptions):
    pass


@dataclasses.dataclass
class SuggestField:
    field: str
    boost: int
    use_ngrams: bool = True
    boost_exact: float = 5
    boost_2gram: float = 1
    boost_3gram: float = 1
    boost_prefix: float = 1


class ICUSuggestParser:
    def __init__(
        self,
        record_cls_or_service_name,
        extra_fields: List[SuggestField] = None,
        default_fields: List[SuggestField] = None,
    ):
        self.record_cls_or_service_name = record_cls_or_service_name
        self.extra_fields = extra_fields or []
        self.default_fields = default_fields or []

    @property
    def record_cls(self):
        if not isinstance(self.record_cls_or_service_name, str):
            return self.record_cls_or_service_name
        return current_service_registry.get(
            self.record_cls_or_service_name
        ).config.record_cls

    def __get__(self, instance, owner):
        search_as_you_type_fields: List[SuggestField] = []
        locale = get_locale()
        if locale:
            language = locale.language

            for fld_name, fld in inspect.getmembers(
                self.record_cls, lambda x: isinstance(x, ICUSuggestField)
            ):
                search_as_you_type_fields.append(
                    SuggestField(f"{fld_name}.{language}.original", 2)
                )
                search_as_you_type_fields.append(
                    SuggestField(f"{fld_name}.{language}.no_accent", 1)
                )

        if not search_as_you_type_fields:
            search_as_you_type_fields.extend(self.default_fields)

        search_as_you_type_fields.extend(self.extra_fields)

        fields = []
        for fld in search_as_you_type_fields:
            fields.append(f"{fld.field}^{fld.boost * fld.boost_exact}")
            if fld.use_ngrams:
                fields.append(f"{fld.field}._2gram^{fld.boost * fld.boost_2gram}")
                fields.append(f"{fld.field}._3gram^{fld.boost * fld.boost_3gram}")
                fields.append(
                    f"{fld.field}._index_prefix^{fld.boost * fld.boost_prefix}"
                )

        return FuzzySuggestQueryParser.factory(fields=fields)


@dataclasses.dataclass
class SortField:
    option_name: str = "title"
    icu_sort_field: str = "sort"
    title: str = _("By Title")


class ICUSortOptions:
    def __init__(self, record_cls_or_service_name, fields: List[SortField] = None):
        self.record_cls_or_service_name = record_cls_or_service_name
        self.fields = fields or [SortField()]

    @property
    def record_cls(self):
        if not isinstance(self.record_cls_or_service_name, str):
            return self.record_cls_or_service_name
        return current_service_registry.get(
            self.record_cls_or_service_name
        ).config.record_cls

    def __get__(self, instance, owner):
        if not inspect.isclass(owner):
            owner = type(owner)
        super_options = {}
        for mro in list(owner.mro())[1:]:
            if hasattr(mro, "sort_options"):
                super_options = mro.sort_options
                break

        ret = {
            **super_options,
            **getattr(owner, "extra_sort_options", {}),
        }

        # transform the sort options by the current language
        locale = get_locale()
        if not locale:
            return ret

        language = locale.language

        for sort_field in self.fields:
            icu_field = getattr(self.record_cls, sort_field.icu_sort_field)
            ret[sort_field.option_name] = {
                "title": sort_field.title,
                "fields": [f"{icu_field.key}.{language}"],
            }
        return ret


class I18nSearchOptions(SearchOptions):
    extra_sort_options = {}
    record_cls = None


class I18nRDMSearchOptions(RDMSearchOptions):
    extra_sort_options = {}
    record_cls = None


class I18nRDMDraftsSearchOptions(RDMSearchDraftsOptions):
    extra_sort_options = {}
    record_cls = None
