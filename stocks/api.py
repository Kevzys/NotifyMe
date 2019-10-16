from stocks.models import Stock, StockList
from rest_framework import viewsets, permissions

from .serializers import StockSerializer, StockListSerializer

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = StockSerializer

class StockListViewSet(viewsets.ModelViewSet):
    queryset = StockList.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = StockListSerializer
