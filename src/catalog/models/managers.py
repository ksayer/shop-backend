from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import QuerySet, OuterRef, Subquery, Value, Min, When, Case
from django.db.models.functions import Coalesce


class ModelQuerySet(QuerySet):
    def for_catalog(self):
        from catalog.models import Product
        color_temperature_subquery = Product.objects.filter(
            model=OuterRef('id'),
            properties__title='color_temperature'
        ).values('model').annotate(
            list_color_temperature=ArrayAgg('properties__value')
        ).values('list_color_temperature')[:1]

        colors_subquery = Product.objects.filter(
            model=OuterRef('id'),
            properties__title='body_color'
        ).values('model').annotate(
            list_body_color=ArrayAgg('properties__color_code')
        ).values('list_body_color')[:1]

        return self.annotate(
            colors=Coalesce(Subquery(colors_subquery), Value([])),
            images=ArrayAgg('products__image__file'),
            min_price=Min('products__price'),
            min_discounted_price=Min('products__discounted_price'),
            color_temperatures=Coalesce(Subquery(color_temperature_subquery), Value([]))
        )


class PropertyQuerySet(QuerySet):
    def with_display_title(self):
        return self.annotate(
            display_title=Case(
                *[When(title=p[0], then=Value(p[1])) for p in self.model.Title.choices],
                default=Value('')
            )
        )
