from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext, Template
from models import Routes
import json

def hello(request):
	return render_to_response('index.html')

def find(request):
	if not request.is_ajax():
		return render_to_response('index.html')
	origin = request.POST['ori']
	destination = request.POST['dest']
	leave_date = request.POST['leave']
	return_date = request.POST['returnd']
	own_car = request.POST['own']
	can_drive = request.POST['can']
	#ALGO HERE YO
	#MAKE THAT SHIT JSON!!!!
	#send it back to js
	message = origin + destination + leave_date + return_date + own_car
	return HttpResponse(json.dumps({"MESSAGE":message}), mimetype="application/json")
	
