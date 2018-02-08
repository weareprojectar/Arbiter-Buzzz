from django.shortcuts import redirect, render
from django.views import View

from stockapi.models import Ticker, OHLCV, Specs
from defacto.models import SupplyDemand, DefactoData


class MarketSignalView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/')
        return render(self.request, 'market_signal.html', {})


class SnapshotView(View):
    def get(self, request, code):
        if not request.user.is_authenticated:
            return redirect('/')
        return render(self.request, 'snapshot.html', {})
