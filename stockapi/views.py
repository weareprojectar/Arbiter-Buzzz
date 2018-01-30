from rest_framework import generics
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from stockapi.models import (
    Info,
    Ticker,
    OHLCV,
    StockInfo,
)
from stockapi.serializers import (
    InfoSerializer,
    TickerSerializer,
    StockInfoSerializer,
    OHLCVSerializer,
)
from utils.paginations import StandardResultPagination


class TickerAPIView(generics.ListCreateAPIView):
    queryset = Ticker.objects.all()
    serializer_class = TickerSerializer
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        queryset = Ticker.objects.all().order_by('id')
        date_by = self.request.GET.get('date')
        code_by = self.request.GET.get('code')
        name_by = self.request.GET.get('name')
        market_by = self.request.GET.get('market_type')
        if date_by:
            queryset = queryset.filter(date=date_by)
        if name_by:
            queryset = queryset.filter(code=name_by)
        if code_by:
            queryset = queryset.filter(date=code_by)
        if market_by:
            queryset = queryset.filter(code=market_by)
        return queryset


class StockInfoAPIView(generics.ListCreateAPIView):
    queryset = StockInfo.objects.all()
    serializer_class = StockInfoSerializer
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        queryset = StockInfo.objects.all().order_by('id')
        date_by = self.request.GET.get('date')
        code_by = self.request.GET.get('code')
        name_by = self.request.GET.get('name')
        market_by = self.request.GET.get('market_type')
        if date_by:
            queryset = queryset.filter(date=date_by)
        if code_by:
            queryset = queryset.filter(code=code_by)
        if name_by:
            queryset = queryset.filter(date=name_by)
        if market_by:
            queryset = queryset.filter(code=market_by)
        return queryset


class OHLCVAPIView(generics.ListCreateAPIView):
    queryset = OHLCV.objects.all()
    serializer_class = OHLCVSerializer
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        queryset = OHLCV.objects.all().order_by('id')
        date_by = self.request.GET.get('date')
        code_by = self.request.GET.get('code')
        name_by = self.request.GET.get('name')
        market_by = self.request.GET.get('market_type')
        if date_by:
            queryset = queryset.filter(date=date_by)
        if code_by:
            queryset = queryset.filter(code=code_by)
        if name_by:
            queryset = queryset.filter(date=name_by)
        if market_by:
            queryset = queryset.filter(code=market_by)
        return queryset


class InfoAPIView(generics.ListCreateAPIView):
    queryset = Info.objects.all()
    serializer_class = InfoSerializer
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self,*args, **kwargs):
        queryset = Info.objects.all().order_by('id')
        date_by = self.request.GET.get('date')
        code_by = self.request.GET.get('code')
        market_by = self.request.GET.get('market_type')
        size_by = self.request.GET.get('size_type')
        style_by = self.request.GET.get('style_type')
        if date_by:
            queryset = queryset.filter(date=date_by)
        if code_by:
            queryset = queryset.filter(code=code_by)
        if market_by:
            queryset = queryset.filter(code=market_by)
        if size_by:
            queryset = queryset.filter(size=size_by)
        if style_by:
            queryset = queryset.filter(style=style_by)
        return queryset
