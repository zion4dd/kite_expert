from kites import models
from django.db.models import Count

class DataMixin:
    paginate_by = 10
    title_page = None
    extra_context = {}

    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page

        self.extra_context['brands'] = models.Brand.objects\
                                            .filter(kite__is_published=True)\
                                            .annotate(Count('kite'))

    # def add_context(self, **kwargs):
    #     context = kwargs
    #     context['brands'] = models.Brand.objects\
    #         .filter(kite__is_published=True)\
    #             .annotate(Count('kite'))
    
    #     if 'brand_selected' not in context:
    #         context['brand_selected'] = 0
        
    #     return context
        