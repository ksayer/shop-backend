from django.db import models
from django.db.models import OuterRef, Subquery

from projects.models import ProjectImage


class ProjectCardQuerySet(models.QuerySet):
    def annotate_main_image(self):
        subquery = ProjectImage.objects.filter(project=OuterRef('project'), main=True)
        return self.annotate(
            main_image_path=Subquery(subquery.values('image__file')[:1]),
            main_image_width=Subquery(subquery.values('image___width')[:1]),
            main_image_height=Subquery(subquery.values('image___height')[:1]),
            main_image_optimized=Subquery(subquery.values('image__optimized')[:1]),
            main_image_id=Subquery(subquery.values('image__id')[:1]),
        )
