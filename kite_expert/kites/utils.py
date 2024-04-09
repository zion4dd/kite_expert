import hashlib
from datetime import datetime

from django.core.cache import cache
from django.db.models import Count

from kites import models


def get_token():
    t = datetime.strftime(datetime.now(), "%d%m%Y%H%M%S")
    return cache.get_or_set(
        key="token",
        default=hashlib.sha256(t.encode()).hexdigest(),
        timeout=600,
    )


class DataMixin:
    paginate_by = 8
    title_page = None
    extra_context = {}

    def __init__(self):
        if self.title_page:
            self.extra_context["title"] = self.title_page

        self.extra_context["brands"] = cache.get_or_set(
            key="brands",
            default=models.Brand.objects.filter(kite__is_published=True).annotate(
                Count("kite")
            ),
            timeout=600,
        )

    # def add_context(self, **kwargs):
    #     context = kwargs
    #     context['brands'] = models.Brand.objects\
    #                               .filter(kite__is_published=True)\
    #                               .annotate(Count('kite'))

    #     if 'brand_selected' not in context:
    #         context['brand_selected'] = 0

    #     return context
