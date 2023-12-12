from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from kites import models
from .serializers import KiteSerializer, ExpertSerializer, BrandSerializer
from .permissions import IsOwnerOrReadOnly


class KiteSet(viewsets.ModelViewSet):
    queryset = models.Kite.objects.all()
    serializer_class = KiteSerializer
    permission_classes = (IsOwnerOrReadOnly, )


class ExpertSet(viewsets.ModelViewSet):
    queryset = models.Expert.objects.all()
    serializer_class = ExpertSerializer
    permission_classes = (IsOwnerOrReadOnly, )


class Brand(generics.ListAPIView):
    serializer_class = KiteSerializer

    def get_queryset(self):
        return models.Kite.objects.filter(brand=self.kwargs['brand_id'])
    

class BrandList(viewsets.ReadOnlyModelViewSet):
    serializer_class = BrandSerializer
    queryset = models.Brand.objects.all()





# class KiteAPI(APIView):
#     def get(self, request):
#         lst = Kite.objects.all().values() # values значения из queryset
#         return Response({'posts': list(lst)})


# class KiteList(generics.ListCreateAPIView):
#     queryset = models.Kite.objects.all()
#     serializer_class = KiteSerializer

    
# class Kite(generics.RetrieveUpdateDestroyAPIView):
#     queryset = models.Kite.objects.all()
#     serializer_class = KiteSerializer
    

    # def get_object(self):
    #     return models.Kite.objects.get(pk=self.kwargs['kite_id'])
    
