from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .funcs import *

@csrf_exempt
def index(request):
	if request.method == 'POST':
		r = json.loads(request.body)
		parse(r)
		return HttpResponse(r)
	else:
		return HttpResponse('ok')
