from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from datetime import datetime
import json
import cPickle as pickle
from django.views.generic import TemplateView, View
import uuid
import jsonpickle
import time
import serial
from core.compiler.compiler import Compiler
import os.path
from os import remove
import subprocess


modules = set(['accel', 'servo', 'led', 'push_button'])

class Accel:
	def __init__(self, x, y):
		self.x_pin = int(x)
		self.y_pin = int(y)
		self.attribs = ['is_up', 'is_down', 'is_left', 'is_right']
		self.name = 'accel'
		self.sense = True

class Servo:
	def __init__(self, data):
		self.data_pin = int(data)
		self.attribs = ['turn_left', 'turn_right', 'center']
		self.name = 'servo'
		self.sense = False

class LED:
	def __init__(self, data):
		self.power = int(data)
		self.attribs = ['turn_on', 'turn_off']
		self.name = 'led'
		self.sense = False

class PushButton:
	def __init__(self, data):
		self.power = int(data)
		self.attribs = ['is_on']
		self.name = 'push_button'
		self.sense = True

def compiler(request):
	payload = json.loads(request.body)
	w_dict = payload['whendo_dict']
	s_list = payload['setup_list']
	i_list = payload['init_list']
	print (w_dict)
	print(s_list)
	print(i_list)

	c1 = Compiler(w_dict, s_list, i_list)
	save_path = '/Users/ankush/blockduino/src/'
	name = 'blockduino_sketch.ino'
	complete_name = os.path.join(save_path, name)
	c1.build(complete_name)
	subprocess.call(['blockduino_script'])
	resp = HttpResponse()
	resp.status_code = 200
	return resp

def new_module(request):
	payload = json.loads(request.body)
	mod_name = payload['name']

	if mod_name not in modules:
		resp = HttpResponse()
		resp.status_code = 401
		return resp
	else:
		if mod_name == 'accel':
			obj = Accel(payload['pin_info'])
		elif mod_name == 'servo':
			obj = Servo(payload['pin_info'])
		elif mod_name == 'led':
			obj = LED(payload['pin_info'])
		else:
			obj = PushButton(payload['pin_info'])

		# retrieve flags lookup
		try:
			flags = pickle.load(open('flags.pick'))
		except IOError:
			flags = {}

		uid = str(int(uuid.uuid4()))
		
		f = open(uid + '.pick', 'w')
		pickle.dump(obj, f)
		f.close()

		flags[uid] = False
		f = open('flags.pick', 'w')
		pickle.dump(flags, f)
		f.close()

		resp = HttpResponse()
		resp.status_code = 200
		return resp

def poll_from_serial(request):
	# TODO get serial
	try:
		remove("slots.pick")
	except OSError:
		pass
	maps = {'0':'led', '3':'switch', '2':'servo', '1':'accel'}
	resps = []
	ser = serial.Serial('/dev/tty.usbmodem14141', 9600)
	while ser.inWaiting() == 0:
		pass
	while ser.inWaiting() != 0:
		resp = ser.readline()
		resps.append(resp)
	resp = resps[-1]
	print resp
	resp = resp.split(';')
	print resp

	try:
		slots = pickle.load(open('slots.pick'))
	except IOError:
		slots = {}

	p_resp = []
	resp = resp[:-1]
	for i in resp:
		d = i.split(',')
		if d[0] in slots:
			if slots[d[0]] == d[1]:
				continue
		else:
			slots[d[0]] = d[1]
			mod_name = maps[d[1]]
			print mod_name
			if mod_name == 'accel':
				obj = Accel(d[2], d[3])
			elif mod_name == 'servo':
				obj = Servo(d[2])
			elif mod_name == 'led':
				obj = LED(d[2])
			else:
				obj = PushButton(d[2])
			p_resp.append(obj)

	f = open('slots.pick', 'w')
	pickle.dump(slots, f)
	f.close()
	print p_resp

	return HttpResponse(jsonpickle.encode(p_resp, unpicklable=False), content_type="application/json")


# API views
class PollingAPIView(View):

	def get(self, *args, **kwargs):
		try:
			flags = pickle.load(open('flags.pick'))
			resp = []
			for key in flags:
				if not flags[key]:
					resp.append(pickle.load(open(key + '.pick')))
					flags[key] = True
			f = open('flags.pick', 'w')
			pickle.dump(flags, f)
			f.close()
		except IOError:
			resp = []

		return HttpResponse(jsonpickle.encode(resp, unpicklable=False), content_type="application/json")

# Rendering views
class HomeView(TemplateView):
	template_name = 'home.html'
