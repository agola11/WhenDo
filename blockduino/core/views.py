from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from core.models import HistoryNode
from datetime import datetime
import json
import cPickle as pickle
from django.views.generic import TemplateView

class Accel:
	def __init__(self):
		pass

class Servo:
	pass

class LED:
	pass

class LEDGroup:
	pass

class PushButton:
	pass

def new_module(request, mod_name):
	modules = set(['accel', 'servo', 'led', 'led_group', 'push_button'])
	if mod_name not in modules:
		resp = HttpResponse()
		resp.status_code = 401
		return resp
	else:
		if mod_name == 'accel':
			pass

class HomeView(TemplateView):
	template_name = 'home.html'
