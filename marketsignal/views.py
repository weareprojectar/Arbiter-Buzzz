from django.shortcuts import redirect, render
from django.views import View

from stockapi.models import Ticker, OHLCV, Specs
from defacto.models import SupplyDemand, DefactoData
from marketsignal.models import MSHome2


class MarketSignalView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/')
        mshome_data = MSHome2.objects.order_by('-date').first()
        return render(self.request, 'market_signal.html', {'mshome_data': mshome_data})


class SnapshotView(View):
    def get(self, request, code):
        if not request.user.is_authenticated:
            return redirect('/')
        ticker_inst = Ticker.objects.filter(code=code)
        name = ticker_inst.first().name if ticker_inst.exists() else ''
        if name != '':
            specs = Specs.objects.filter(code=code).order_by('-date').first()
            defacto_data = DefactoData.objects.filter(code=code).order_by('-date').first()
            scores = {
                'sd': int(defacto_data.score),
                'mom': int(specs.momentum_score),
                'vol': int(specs.volatility_score),
                'cor': int(specs.correlation_score)
            }
            total = (scores['sd'] + scores['mom'] + scores['vol'] + scores['cor'])//4
            scores['total'] = total

            sd = SupplyDemand.objects.filter(code=code).order_by('-date').first()
            avg_price = {
                'institution': int(sd.institution_average_price),
                'foreigner': int(sd.foreigner_average_price)
            }
        else:
            scores = {}
        context = {
            'name': name,
            'code': code,
            'average_price': avg_price,
            'scores': scores
        }
        return render(self.request, 'snapshot.html', context)
