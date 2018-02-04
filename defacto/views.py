from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from defacto.models import SupplyDemand, Defacto
from defacto.serializers import SupplyDemandSerializer, DefactoSerializer
from utils.paginations import StandardResultPagination


class SupplyDemandAPIView(generics.ListCreateAPIView):
    queryset = SupplyDemand.objects.all()
    serializer_class = SupplyDemandSerializer
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        queryset = SupplyDemand.objects.all().order_by('id')
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


class DefactoAPIView(generics.ListCreateAPIView):
    queryset = Defacto.objects.all()
    serializer_class = DefactoSerializer
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        queryset = Defacto.objects.all().order_by('id')
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
