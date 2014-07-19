from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from datetime import datetime
import json
import cPickle as pickle
from django.views.generic import TemplateView, View
import uuid
import jsonpickle

modules = set(['accel', 'servo', 'led', 'push_button'])

class Accel:
	def __init__(self, data):
		self.data_pin = data['data_pin']
		self.power = data['power_pin']
		self.ground = data['ground_pin']
		self.attribs = ['turn_up', 'turn_down', 'turn_left', 'turn_right']

class Servo:
	def __init__(self, data):
		self.data_pin = data['data_pin']
		self.power = data['power_pin']
		self.ground = data['ground_pin']
		self.attribs = ['rotate_left', 'rotate_right', 'center']

class LED:
	def __init__(self, data):
		self.power = data['power_pin']
		self.ground = data['ground_pin']
		self.attribs = ['turn_on', 'turn_off']

class PushButton:
	def __init__(self, data):
		self.power = data['power_pin']
		self.ground = data['ground_pin']
		self.attribs = ['turn_on', 'turn_off']

def new_module(request):
	payload = json.loads(request.body)
	mod_name = payload['name']

	if mod_name not in modules:
		resp = HttpResponse()
		resp.status_code = 401
		return resp
	else:
		if mod_name == 'accel':
			accel = Accel(payload['pin_info'])
			#save in fs
		elif mod_name == 'servo':
			servo = Servo(payload['pin_info'])
			#save in fs
		elif mod_name == 'led':
			led = LED(payload['pin_info'])
			#save in fs
		else:
			push_button = PushButton(payload['pin_info'])
			#save in fs


# API views
class PollingAPIView(View):

	def get(self, *args, **kwargs):
		return HttpResponse(json.dumps({'test': True}), content_type="application/json")

# Rendering views
class HomeView(TemplateView):
	template_name = 'home.html'
