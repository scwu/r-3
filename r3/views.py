from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.shortcuts import render_to_response

def hello(request):
	return render_to_response('index.html')

def find(request):
	if not request.POST:
		return render_to_response('index.html')
	origin = request.POST['ori']
	destination = request.POST['dest']
	leave_date = request.POST['leave']
	return_date = request.POST['return_d']
	own_car = request.POST['own']
	can_drive = request.POST['can_drive']
	#ALGO HERE YO
	#MAKE THAT SHIT JSON!!!!
	#send it back to js
	
