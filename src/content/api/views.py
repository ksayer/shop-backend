from django.db.models import Prefetch
from rest_framework import generics

from content.api.serializers import ContentBlockSerializer
from content.models import Banner, ContentBlock, ModelCard, ProjectCard, FeedbackCard

from django.db import connection
from django.db import reset_queries


def database_debug(func):
    def inner_func(*args,**kwargs):
        reset_queries()
        results=func(*args,**kwargs)
        query_info=connection.queries
        print('function_name:{}'.format(func.__name__))
        print('query_count:{}'.format(len(query_info)))
        queries=['{} - {}\n'.format(query['time'], query['sql'])for query in query_info]
        print('queries:\n{}'.format(''.join(queries)))
        return results
    return inner_func


class ContentBlockListAPIView(generics.ListAPIView):
    queryset = ContentBlock.objects.prefetch_related(
        Prefetch('banners', Banner.objects.select_related('image').prefetch_related('buttons')),
        Prefetch('modelcards', ModelCard.objects.select_related('model__image')),
        Prefetch(
            'feedbackcards',
            FeedbackCard.objects.select_related('feedback__avatar', 'feedback__project')
        ),
        Prefetch(
            'projectcards', ProjectCard.objects.select_related('project').annotate_main_image()
        ),
    )

    serializer_class = ContentBlockSerializer
    filterset_fields = ['page__slug']

    @database_debug
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
