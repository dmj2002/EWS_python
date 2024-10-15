import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from predict import service


# Create your views here.
def index(request):
    return HttpResponse("Hello")
# @csrf_exempt
def train(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # 从 JSON 数据中获取字段值
        train_points = data.get('train_point')
        test_points = data.get('test_point')
        # train_points = [point for point in data.get('train_point', [])]
        # test_points = [point for point in data.get('test_point', [])]
        try:
            msg = service.train_model(train_points, test_points)
            return JsonResponse({'status': 'success', 'messaeg': msg})
        except Exception as e:
            return JsonResponse({'status': str(e)})


def predict(request):
    return HttpResponse('Predicting...')