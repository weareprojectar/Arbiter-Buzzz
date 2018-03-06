from django.shortcuts import render
from django.views import View
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter

from defacto.models import AgentData, ScoreData
from defacto.api.serializers import AgentDataSerializer, ScoreDataSerializer

from utils.paginations import StandardResultPagination


class AgentDataAPIView(generics.ListCreateAPIView):
    queryset = AgentData.objects.all()
    serializer_class = AgentDataSerializer
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        queryset = AgentData.objects.all().order_by('id')
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


class ScoreDataAPIView(generics.ListCreateAPIView):
    queryset = ScoreData.objects.all()
    serializer_class = ScoreDataSerializer
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        queryset = ScoreData.objects.all().order_by('id')
        date_by = self.request.GET.get('date')
        code_by = self.request.GET.get('code')
        if date_by:
            queryset = queryset.filter(date=date_by)
        if code_by:
            queryset = queryset.filter(code=code_by)
        return queryset
