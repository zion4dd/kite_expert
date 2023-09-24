from kites import models
from django.db.models import Count

class DataMixin:
    paginate_by = 30

    def get_user_context(self, **kwargs):
        context = kwargs
        context['brands'] = models.Brand.objects\
            .filter(kite__is_published=True)\
                .annotate(Count('kite'))
    
        # if 'brand_selected' not in context:
        #     context['brand_selected'] = 0
        
        return context
        