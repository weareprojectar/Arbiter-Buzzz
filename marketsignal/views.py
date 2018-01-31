from django.shortcuts import redirect, render
from django.views import View


class MarketSignalView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/')
        return render(self.request, 'market_signal.html', {})
