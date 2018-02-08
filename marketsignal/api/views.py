from rest_framework import generics
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from marketsignal.models import Index
from marketsignal.api.serializers import IndexSerializer

from utils.paginations import StandardResultPagination


class IndexAPIView(generics.ListCreateAPIView):
    queryset = Index.objects.all()
    serializer_class = IndexSerializer
    # pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        queryset = Index.objects.all().order_by('id')
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


class TopIndustryAPIView(generics.ListAPIView):
    serializer_class = IndexSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = Index.objects.filter(category='I').order_by('id')
        start = self.request.GET.get('start')
        end = self.request.GET.get('end')
        rank = self.request.GET.get('rank')
        if start and end:
            queryset = queryset.filter(date__gte=start).filter(date__lte=end)
        if rank:
            last_date = queryset.last().date
            ranked_index = queryset.filter(date=last_date).order_by('-index')[int(rank)-1].name
            queryset = queryset.filter(name=ranked_index)
        return queryset
