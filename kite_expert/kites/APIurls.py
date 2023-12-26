from django.urls import path, include, re_path
from rest_framework import routers
from kites.APIviews import KiteSet, Brand, BrandList, ExpertSet


kite_router = routers.SimpleRouter()
expert_router = routers.SimpleRouter()
brand_router = routers.SimpleRouter()

kite_router.register(r'kite', KiteSet)
expert_router.register(r'expert', ExpertSet)
brand_router.register(r'brand', BrandList)

urlpatterns = [
    path('auth/', include('rest_framework.urls')),

    path('kite/brand/<int:brand_id>/', Brand.as_view()),
    
    path('', include(kite_router.urls)),
    path('', include(brand_router.urls)),
    path('', include(expert_router.urls)),

    re_path(r'^auth/', include('djoser.urls')),  # auth/login
    re_path(r'^auth/', include('djoser.urls.authtoken')),  # auth/token/login
]
