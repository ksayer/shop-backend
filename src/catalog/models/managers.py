from django.conf import settings
from django.contrib.postgres.aggregates import JSONBAgg
from django.db.models import Case, F, Min, Q, QuerySet, Value, When
from django.db.models.functions import Concat, JSONObject


def get_filter_aggregations(prefix: str = '') -> dict[str, JSONObject]:
    """
    Prepare aggregation JSONObjects for annotate filters
    """
    aggregations = {}
    properties = ['power', 'color_temperature', 'beam_angle', 'beam', 'dimming', 'protection']
    for prop in properties:
        property_id = f"{prefix}models__modifications__products__property__{prop}__id"
        property_group = f"{prefix}models__modifications__products__property__{prop}__group__title"
        property_title = f"{prefix}models__modifications__products__property__{prop}__title"

        aggregations[prop] = JSONBAgg(
            JSONObject(
                id=property_id,
                group_title=property_group
            ),
            distinct=True,
            filter=~Q(**{property_title: None})
        )
    return aggregations


class GroupQuerySet(QuerySet):
    filters_agg = get_filter_aggregations('categories__')

    def annotate_filters(self):
        return self.annotate(filters=JSONObject(**self.filters_agg))


class CategoryQuerySet(QuerySet):
    filters_agg = get_filter_aggregations()

    def annotate_filters(self):
        return self.annotate(filters=JSONObject(**self.filters_agg))


class ModelQuerySet(QuerySet):
    def for_catalog(self):
        return self.annotate(
            min_price=Min('modifications__products__price'),
            min_discounted_price=Min('modifications__products__discounted_price'),
            _color_temperatures=JSONBAgg(
                'modifications__products__property__color_temperature__title',
                distinct=True,
            ),
            color_temperatures=Case(
                When(_color_temperatures=[None], then=Value([])),
                default='_color_temperatures'
            ),
            images=JSONBAgg(
                JSONObject(
                    id=F('modifications__products__id'),
                    ordering=F('modifications__products__ordering'),
                    file=Concat(
                        Value(f'{settings.HOST_DOMAIN}/media/'), F('modifications__products__image__file')
                    ),
                    width=F('modifications__products__image___width'),
                    height=F('modifications__products__image___height'),
                    color=F('modifications__products__property__body_color__color'),
                ),
                ordering='modifications__products__ordering',
            ),
        )
