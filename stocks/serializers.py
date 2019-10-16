from rest_framework import serializers
from stocks.models import Stock, StockList

class StockSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stock
        fields = '__all__'

class StockListSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockList
        fields = '__all__'
