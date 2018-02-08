from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from stockapi.models import (
    BM,
    Ticker,
    StockInfo,
    Specs,
    OHLCV,
    Info,
    Financial,
    FinancialRatio,
    QuarterFinacial,
    BuySell,
)
from stockapi.serializers import (
    BMSerializer,
    CandleSerializer,
    TickerSerializer,
    StockInfoSerializer,
    SpecsSerializer,
    OHLCVSerializer,
    InfoSerializer,
    FinancialSerializer,
    FinancialRatioSerializer,
    QuarterFinacialSerializer,
    BuySellSerializer,
)
from utils.paginations import StandardResultPagination, OHLCVPagination
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class BMAPIView(generics.ListCreateAPIView):
    from stockapi.models import BM
    queryset = BM.objects.all()
    serializer_class = BMSerializer
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        queryset = BM.objects.all().order_by('id')
        date_by = self.request.GET.get('date')
        start = self.request.GET.get('start')
        end = self.request.GET.get('end')
        name_by = self.request.GET.get('name')
        category_by = self.request.GET.get('category')
        if date_by:
            queryset = queryset.filter(date=date_by)
        if start and end and not date_by:
            queryset = queryset.filter(date__gte=start).filter(date__lte=end)
        if name_by:
            queryset = queryset.filter(name=name_by)
        if category_by:
            queryset = queryset.filter(category=category_by)
        return queryset


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
            queryset = queryset.filter(name=name_by)
        if code_by:
            queryset = queryset.filter(code=code_by)
        if market_by:
            queryset = queryset.filter(market=market_by)
        return queryset


class TickerUpdatedAPIView(APIView):
    serializer_class = TickerSerializer

    def get(self, request, *args, **kwargs):
        recent_ticker = Ticker.objects.order_by('-id').first()
        updated_date = recent_ticker.date
        return Response({'updated_date': updated_date}, status=HTTP_200_OK)


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
            queryset = queryset.filter(name=name_by)
        if market_by:
            queryset = queryset.filter(market=market_by)
        return queryset


class SpecsAPIView(generics.ListCreateAPIView):
    queryset = Specs.objects.all()
    serializer_class = SpecsSerializer
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        queryset = Specs.objects.all().order_by('id')
        date_by = self.request.GET.get('date')
        code_by = self.request.GET.get('code')
        if date_by:
            queryset = queryset.filter(date=date_by)
        if code_by:
            queryset = queryset.filter(code=code_by)
        return queryset


class OHLCVAPIView(generics.ListCreateAPIView):
    queryset = OHLCV.objects.all()
    serializer_class = OHLCVSerializer
    pagination_class = OHLCVPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        queryset = OHLCV.objects.all().order_by('id')
        date_by = self.request.GET.get('date')
        start = self.request.GET.get('start')
        end = self.request.GET.get('end')
        code_by = self.request.GET.get('code')
        if date_by:
            queryset = queryset.filter(date=date_by)
        if start and end and not date_by:
            queryset = queryset.filter(date__gte=start).filter(date__lte=end)
        if code_by:
            queryset = queryset.filter(code=code_by)
        return queryset


# class OHLCVNoPageAPIView(generics.ListCreateAPIView):
#     queryset = OHLCV.objects.all()
#     serializer_class = OHLCVSerializer
#     filter_backends = [SearchFilter, OrderingFilter]
#
#     def get_queryset(self, *args, **kwargs):
#         queryset = OHLCV.objects.all().order_by('id')
#         date_by = self.request.GET.get('date')
#         start = self.request.GET.get('start')
#         end = self.request.GET.get('end')
#         code_by = self.request.GET.get('code')
#         if date_by:
#             queryset = queryset.filter(date=date_by)
#         if start and end and not date_by:
#             queryset = queryset.filter(date__gte=start).filter(date__lte=end)
#         if code_by:
#             queryset = queryset.filter(code=code_by)
#         return queryset


class CandleAPIView(APIView):
    serializer_class = CandleSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = CandleSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            code = serializer.data['code']
            candle_data = OHLCV.objects.filter(code=code)
            candle_data = candle_data.values_list('date', 'open_price', 'high_price', 'low_price', 'close_price', 'volume')
            return Response({'candle_data': candle_data}, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class InfoAPIView(generics.ListCreateAPIView):
    queryset =Info.objects.all()
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


class FinancialAPIView(generics.ListCreateAPIView):
    queryset = Financial.objects.all()
    serializer_class = FinancialSerializer
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        queryset = Financial.objects.all().order_by('id')
        date_by = self.request.GET.get('date')
        code_by = self.request.GET.get('code')
        name_by = self.request.GET.get('name')
        if date_by:
            queryset = queryset.filter(date=date_by)
        if name_by:
            queryset = queryset.filter(name=name_by)
        if code_by:
            queryset = queryset.filter(code=code_by)
        return queryset


class FinancialRatioAPIView(generics.ListCreateAPIView):
    queryset = FinancialRatio.objects.all()
    serializer_class = FinancialRatioSerializer
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        queryset = FinancialRatio.objects.all().order_by('id')
        date_by = self.request.GET.get('date')
        code_by = self.request.GET.get('code')
        name_by = self.request.GET.get('name')
        if date_by:
            queryset = queryset.filter(date=date_by)
        if name_by:
            queryset = queryset.filter(name=name_by)
        if code_by:
            queryset = queryset.filter(code=code_by)
        return queryset


class QuarterFinacialAPIView(generics.ListCreateAPIView):
    queryset = QuarterFinacial.objects.all()
    serializer_class = QuarterFinacialSerializer
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        queryset = QuarterFinacial.objects.all().order_by('id')
        date_by = self.request.GET.get('date')
        code_by = self.request.GET.get('code')
        name_by = self.request.GET.get('name')
        if date_by:
            queryset = queryset.filter(date=date_by)
        if name_by:
            queryset = queryset.filter(name=name_by)
        if code_by:
            queryset = queryset.filter(code=code_by)
        return queryset


class BuySellAPIView(generics.ListCreateAPIView):
    queryset = BuySell.objects.all()
    serializer_class = BuySellSerializer
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        queryset = BuySell.objects.all().order_by('id')
        date_by = self.request.GET.get('date')
        code_by = self.request.GET.get('code')
        name_by = self.request.GET.get('name')
        if date_by:
            queryset = queryset.filter(date=date_by)
        if name_by:
            queryset = queryset.filter(name=name_by)
        if code_by:
            queryset = queryset.filter(code=code_by)
        return queryset
