from rest_framework import generics
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from marketsignal.models import Index
from marketsignal.api.serializers import IndexSerializer

from utils.paginations import StandardResultPagination


class IndexAPIView(generics.ListCreateAPIView):
    queryset = Index.objects.all()
    serializer_class = IndexSerializer
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        queryset = Index.objects.all().order_by('id')
        date_by = self.request.GET.get('date')
        name_by = self.request.GET.get('name')
        category_by = self.request.GET.get('category')
        if date_by:
            queryset = queryset.filter(date=date_by)
        if name_by:
            queryset = queryset.filter(name=name_by)
        if category_by:
            queryset = queryset.filter(category=category_by)
        return queryset
