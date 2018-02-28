from django.shortcuts import render
from django.views import View
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from defacto.models import (
    SupplyDemand,
    DefactoData,
    AgentData,
    ScoreData,
)
from defacto.serializers import (
    SupplyDemandSerializer,
    DefactoSerializer,
    AgentDataSerializer,
    ScoreDataSerializer,
)
from utils.paginations import StandardResultPagination


class ScannerView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/')
        return render(self.request, 'scanner.html', {})


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
    queryset = DefactoData.objects.all()
    serializer_class = DefactoSerializer
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        queryset = DefactoData.objects.all().order_by('id')
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


class AgentDataAPIView(generics.ListCreateAPIView):
    queryset = AgentData.objects.all()
    serializer_class = AgentDataSerializer
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        queryset = AgentData.objects.all().order_by('id')
        date_by = self.request.GET.get('date')
        code_by = self.request.GET.get('code')
        if date_by:
            queryset = queryset.filter(date=date_by)
        if code_by:
            queryset = queryset.filter(code=code_by)
        return queryset


class ScoreDataAPIView(generics.ListCreateAPIView):
    queryset = ScoreData.objects.all()
    serializer_class = ScoreDataSerializer
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        queryset = ScoreData.objects.all().order_by('id')
        date_by = self.request.GET.get('date')
        code_by = self.request.GET.get('code')
        lead_agent_by = self.request.GET.get('lead_agent')
        if date_by:
            queryset = queryset.filter(date=date_by)
        if code_by:
            queryset = queryset.filter(code=code_by)
        if lead_agent_by:
            queryset = queryset.filter(lead_agent=lead_agent_by)
        return queryset
