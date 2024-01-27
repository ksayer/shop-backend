from django.conf import settings
from django.contrib.postgres.aggregates import ArrayAgg, JSONBAgg
from django.db.models import Case, F, Min, OuterRef, Q, QuerySet, Subquery, Value, When
from django.db.models.functions import Coalesce, Concat, JSONObject


class GroupQuerySet(QuerySet):
    def annotate_filters(self):
        return self
        property_title_conditions = [
            When(categories__models__products__properties__title=title, then=Value(label))
            for title, label in Property.Title.choices
        ]
        return self.annotate(
            filters=JSONBAgg(
                JSONObject(
                    property=F('categories__models__products__properties__group__title'),
                    slug=F('categories__models__products__properties__title'),
                    title=Case(*property_title_conditions),
                    id=F('categories__models__products__properties__group__id'),
                ),
                filter=~Q(categories__models__products__properties__group__title=None),
                distinct=True,
            )
        )


class ModelQuerySet(QuerySet):
    def for_catalog(self):
        from catalog.models import Product
        return self
        color_temperature_subquery = (
            Product.objects.filter(model=OuterRef('id'), properties__title='color_temperature')
            .values('model')
            .annotate(list_color_temperature=ArrayAgg('properties__value'))
            .values('list_color_temperature')[:1]
        )

        return self.filter(products__properties__title='body_color').annotate(
            min_price=Min('products__price'),
            min_discounted_price=Min('products__discounted_price'),
            color_temperatures=Coalesce(Subquery(color_temperature_subquery), Value([])),
            images=JSONBAgg(
                JSONObject(
                    id=F('products__id'),
                    ordering=F('products__ordering'),
                    file=Concat(
                        Value(f'{settings.HOST_DOMAIN}/media/'), F('products__image__file')
                    ),
                    width=F('products__image___width'),
                    height=F('products__image___height'),
                    color=F('products__properties__color_code'),
                ),
                ordering='products__ordering',
            ),
        )


class PropertyQuerySet(QuerySet):
    def with_display_title(self):
        return self.annotate(
            display_title=Case(
                *[When(title=p[0], then=Value(p[1])) for p in self.model.Title.choices],
                default=Value(''),
            )
        )
