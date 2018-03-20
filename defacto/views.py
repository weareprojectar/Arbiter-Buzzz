from django.shortcuts import render, redirect
from django.views import View

from defacto.models import RankData


class ScannerView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/')
        categories = ['institution_score', 'foreigner_score', 'total_increase', 'institution_increase', 'foreigner_increase']
        context = {}
        for category in categories:
            if 'score' in category:
                data = RankData.objects.filter(cartegory=category)[0:10]
            else:
                data = RankData.objects.filter(cartegory=category)[0:6]
            context[category] = data
        return render(self.request, 'scanner.html', context)
