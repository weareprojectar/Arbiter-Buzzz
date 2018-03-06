from django.shortcuts import render, redirect
from django.views import View


class ScannerView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/')
        return render(self.request, 'scanner.html', {})
