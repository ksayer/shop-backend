from django.db.models import Prefetch
from rest_framework import generics

from content.api.serializers import ContentBlockSerializer
from content.models import (
    Banner,
    ContentBlock,
    FeedbackCard,
    ModelCard,
    ProjectCard,
    Publication, Tab,
)


class ContentBlockListAPIView(generics.ListAPIView):
    queryset = ContentBlock.objects.prefetch_related(
        Prefetch(
            'banners',
            Banner.objects.select_related('image').prefetch_related(
                'buttons',
                Prefetch('tabs', Tab.objects.select_related('image'))
            )
        ),
        Prefetch('modelcards', ModelCard.objects.select_related('model__image')),
        Prefetch(
            'feedbackcards',
            FeedbackCard.objects.select_related('feedback__avatar', 'feedback__project'),
        ),
        Prefetch(
            'projectcards', ProjectCard.objects.select_related('project').annotate_main_image()
        ),
        Prefetch('publications', Publication.objects.select_related('image')),
        Prefetch(
            'banners',
            Banner.objects.select_related('image')
            .filter(type=Banner.Type.CONSULTANT)
            .order_by('?'),
            to_attr='consultant',
        ),
    )

    serializer_class = ContentBlockSerializer
    filterset_fields = ['page__slug']
