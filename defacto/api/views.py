from django.shortcuts import render
from django.views import View
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter

from defacto.models import AgentData, ScoreData, RankData
from defacto.api.serializers import (
                        AgentDataSerializer,
                        ScoreDataSerializer,
                        RankDataSerializer,
                        )
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


class RankDataAPIView(generics.ListCreateAPIView):
    queryset = RankData.objects.all()
    serializer_class = RankDataSerializer
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        queryset = RankData.objects.all()
        date_by = self.request.GET.get('date')
        code_by = self.request.GET.get('code')
        category = self.request.GET.get('category')
        rankpage = self.request.GET.get('rankpage')
        items_per_page = 0
        if date_by:
            queryset = queryset.filter(date=date_by)
        if code_by:
            queryset = queryset.filter(code=code_by)
        if category:
            queryset = queryset.filter(cartegory=category)
            items_per_page = 10 if 'score' in category else 6
        if rankpage:
            start_index = (int(rankpage) - 1) * items_per_page
            end_index = int(rankpage) * items_per_page
            queryset = queryset.order_by('id')[start_index:end_index]
        return queryset
