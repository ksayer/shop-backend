from django.conf import settings
from django.contrib.postgres.aggregates import ArrayAgg, JSONBAgg
from django.db.models import QuerySet, OuterRef, Subquery, Value, Min, When, Case, F
from django.db.models.functions import Coalesce, JSONObject, Concat


class ModelQuerySet(QuerySet):
    def for_catalog(self):
        from catalog.models import Product
        color_temperature_subquery = Product.objects.filter(
            model=OuterRef('id'),
            properties__title='color_temperature'
        ).values('model').annotate(
            list_color_temperature=ArrayAgg('properties__value')
        ).values('list_color_temperature')[:1]

        return self.filter(products__properties__title='body_color').annotate(
            min_price=Min('products__price'),
            min_discounted_price=Min('products__discounted_price'),
            color_temperatures=Coalesce(Subquery(color_temperature_subquery), Value([])),
            images=JSONBAgg(JSONObject(
                id=F('products__id'),
                ordering=F('products__ordering'),
                file=Concat(Value(f'{settings.HOST_DOMAIN}/media/'), F('products__image__file')),
                width=F('products__image___width'),
                height=F('products__image___height'),
                color=F('products__properties__color_code')
            ), ordering='products__ordering'),
        )


class PropertyQuerySet(QuerySet):
    def with_display_title(self):
        return self.annotate(
            display_title=Case(
                *[When(title=p[0], then=Value(p[1])) for p in self.model.Title.choices],
                default=Value('')
            )
        )
