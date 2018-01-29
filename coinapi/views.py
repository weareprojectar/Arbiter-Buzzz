from rest_framework import generics
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from coinapi.models import Candle, Price, MM
from coinapi.serializers import (
    CandleSerializer,
    PriceSerializer,
    CandleMMSerializer,
)
from utils.paginations import StandardResultPagination


class CandleAPIView(generics.ListCreateAPIView):
    queryset = Candle.objects.all()
    serializer_class = CandleSerializer
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        queryset = Candle.objects.all().order_by('id')
        date_by = self.request.GET.get('date')
        ticker_by = self.request.GET.get('ticker')
        if date_by and ticker_by:
            queryset_list = queryset.filter(date=date_by).filter(ticker=ticker_by)
            return queryset_list
        if date_by and not ticker_by:
            queryset_list = queryset.filter(date=date_by)
            return queryset_list
        if ticker_by and not date_by:
            queryset_list = queryset.filter(ticker=ticker_by)
            return queryset_list
        return queryset


class CandleDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Candle.objects.all()
    serializer_class = CandleSerializer


class PriceAPIView(generics.ListCreateAPIView):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        queryset = Price.objects.all().order_by('id')
        date_by = self.request.GET.get('date')
        ticker_by = self.request.GET.get('ticker')
        if date_by and ticker_by:
            queryset_list = queryset.filter(date=date_by).filter(tikcer=ticker_by)
            return queryset_list
        if date_by and not ticker_by:
            queryset_list = queryset.filter(date=date_by)
            return queryset_list
        if ticker_by and not date_by:
            queryset_list = queryset.filter(ticker=ticker_by)
            return queryset_list
        return queryset


class PriceDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer


class MMAPIView(generics.ListAPIView):
    queryset = MM.objects.all()
    serializer_class = CandleMMSerializer
    filter_backends = [SearchFilter, OrderingFilter]

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = CandleMMSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            ticker = serializer.data['ticker']
            start = serializer.data['start']
            end = serializer.data['end']
            mm_num = serializer.data['mm_num']
            candles = Candle.objects.filter(ticker=ticker).filter(date__gte=start).filter(date__lte=end)
            candles = candles.order_by('mean_price')

            local_min = candles.values_list('mean_price')[0][0]
            local_max = candles.values_list('mean_price')[len(candles)-1][0]
            local_width = local_max - local_min

            mm_width = local_width/mm_num
            mm= [0]*mm_num

            candles_num = len(candles)

            target = local_min + mm_width
            sub_vol = 0
            total_vol = 0
            step = 0

            for idx in range(candles_num):
                if candles.values_list('mean_price')[idx][0] > target :
                    target += mm_width
                    mm[step] = sub_vol
                    sub_vol = 0
                    step += 1
                if step == mm_num :
                    break
                sub_vol += candles.values_list('volume')[idx][0]
                total_vol += candles.values_list('volume')[idx][0]

                if idx == candles_num -1 :
                    mm[step] = sub_vol

            mm = [(elem/total_vol)*100 for elem in mm]

            result = {
                'result': mm
            }
            return Response(result, status=200)

    # def get_queryset(self, *args, **kwargs):
    #     queryset = Candle.objects.all()
    #     ticker_by = self.request.GET.get('ticker')
    #     start = self.request.GET.get('start')
    #     end = self.request.GET.get('end')
    #     mm_num = self.request.GET.get('mm_num')
    #     queryset = queryset.filter(date__gte=start).filter(date__lte=end).filter(ticker=ticker_by)
    #     candles = queryset.order_by("mp")
    #
    #     local_min = candles.values_list('mp')[0][0]
    #     local_max = candles.values_list('mp')[len(candles)-1][0]
    #     local_width = local_max - local_min
    #
    #     mm_width = local_width/mm_num
    #     mm= [0]*mm_num
    #
    #     candles_num = len(candles)
    #
    #     target = local_min + mm_width
    #     sub_vol = 0
    #     total_vol = 0
    #     step = 0
    #
    #     for idx in range(candles_num):
    #         if candles.values_list('mp')[idx][0] > target :
    #             target += mm_width
    #             mm[step] = sub_vol
    #             sub_vol = 0
    #             step += 1
    #         if step == mm_num :
    #             break
    #         sub_vol += candles.values_list('vol')[idx][0]
    #         total_vol += candles.values_list('vol')[idx][0]
    #
    #     return mm
