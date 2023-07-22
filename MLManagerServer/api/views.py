from django.http import JsonResponse
from django.views import View


class ExperimentsView(View):
    def get(self, request):
        return JsonResponse({'status': 200, 'code': 10000, 'msg': 'ok'})


class ExperimentsListView(View):
    def get(self, request):
        return JsonResponse({'status': 200, 'code': 10000, 'msg': 'ok'})
    
class ExpParametersView(View):
    def get(self, request):
        return JsonResponse({'status': 200, 'code': 10000, 'msg': 'ok'})
    
class ExpMetricsView(View):
    def get(self, request):
        return JsonResponse({'status': 200, 'code': 10000, 'msg': 'ok'})

class ExpModelsView(View):
    def get(self, request):
        return JsonResponse({'status': 200, 'code': 10000, 'msg': 'ok'})


class DownloadModelsView(View):
    def get(self, request):
        return JsonResponse({'status': 200, 'code': 10000, 'msg': 'ok'})
