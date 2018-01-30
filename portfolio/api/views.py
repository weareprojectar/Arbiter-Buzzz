from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt

from portfolio.api.serializers import (
    PortfolioDiagnosisSerializer,
    PortfolioOptimizationSerializer,
    PortfolioRatioSerializer,
    PortfolioSerializer,
    PortfolioHistorySerializer,
    TodayPortfolioSerializer,
)
from portfolio.models import (
    Portfolio,
    PortfolioHistory,
    PortfolioDiagnosis,
    TodayPortfolio,
)
from buzzzapi.models import (
    Ticker,
)
from utils.paginations import UserResultPagination, StandardResultPagination

User = get_user_model()

from rest_framework.authentication import SessionAuthentication, BasicAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


# @method_decorator(csrf_exempt, name='dispatch')
class PortfolioAPIView(generics.ListCreateAPIView):
    queryset = Portfolio.objects.all().order_by('-id')
    serializer_class = PortfolioSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication_classes = (CsrfExemptSessionAuthentication,)
    pagination_class = StandardResultPagination

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PortfolioDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data.copy()
        data['user'] = request.user
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class TodayPortfolioAPIView(generics.ListCreateAPIView):
    queryset = TodayPortfolio.objects.all()
    serializer_class = TodayPortfolioSerializer


class TodayPortfolioDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TodayPortfolio.objects.all()
    serializer_class = TodayPortfolioSerializer


class PortfolioDiagnosisAPIView(generics.RetrieveAPIView):
    queryset = Portfolio
    serializer_class = PortfolioDiagnosisSerializer


class PortfolioRatioAPIView(generics.ListCreateAPIView):
    queryset = PortfolioDiagnosis.objects.all()
    serializer_class = PortfolioRatioSerializer


class PortfolioOptimizationAPIView(generics.RetrieveAPIView):
    queryset = Portfolio
    serializer_class = PortfolioOptimizationSerializer


class PortfolioHistoryAPIView(generics.ListCreateAPIView):
    queryset = PortfolioHistory.objects.all()
    serializer_class = PortfolioHistorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication_classes = (CsrfExemptSessionAuthentication,)
    pagination_class = StandardResultPagination

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['portfolio'] = Portfolio.objects.get(id=data['portfolio']).id
        ticker = Ticker.objects.filter(code=data['code']).order_by('-id').first()
        data['code'] = ticker.id
        data['date'] = ticker.date
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PortfolioHistoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PortfolioHistory.objects.all()
    serializer_class = PortfolioHistorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
