from datetime import datetime

from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from portfolio.models import Portfolio, PortfolioHistory
from stockapi.models import Ticker, OHLCV, Info


@method_decorator(csrf_exempt, name='dispatch')
class RMSHomeView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/')
        return render(self.request, 'rms_main.html', {})


@method_decorator(csrf_exempt, name='dispatch')
class RMSStartView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/')
        return render(self.request, 'rms_start.html', {})


class RMSDiagnosisView(View):
    def get(self, request, pk):
        if not request.user.is_authenticated:
            return redirect('/')
        portfolio = Portfolio.objects.filter(pk=pk)
        if portfolio.exists():
            if portfolio.first().user == request.user:
                context = {'status': '진단'}
            else:
                context = {
                    'status': '진단',
                    'portfolio': portfolio.first(),
                    'date': datetime.now()
                }
        return render(self.request, 'rms_opt.html', context)


class RMSOptimizationView(View):
    def get(self, request, pk):
        if not request.user.is_authenticated:
            return redirect('/')
        portfolio = Portfolio.objects.filter(pk=pk)
        if portfolio.exists():
            if portfolio.first().user == request.user:
                context = {'status': '최적화'}
            else:
                context = {
                    'status': '최적화',
                    'portfolio': portfolio.first(),
                    'date': datetime.now()
                }
        return render(self.request, 'rms_final.html', context)


class RMSTodayPortfolioView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/')
        context = {'status': '오늘의 포트폴리오'}
        return render(self.request, 'rms_today.html', context)
