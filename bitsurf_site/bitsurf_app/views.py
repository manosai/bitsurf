# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

import boto.sdb
import json
import os

def aws_connect():
	conn = boto.sdb.connect_to_region('us-west-2',\
		aws_access_key_id=os.environ['aws_access_key_id'], \
		aws_secret_access_key=os.environ['aws_secret_access_key'])
	return conn

def home(request):
    return render_to_response('login.html', {}, RequestContext(request))

def add_user(request):
	if request.method == 'GET':
		conn = aws_connect()
		user_domain = conn.get_domain('user_table')
		bitcoin_address = request['bitcoin_addr']
		current_attrs = user_domain.get_item(bitcoin_address, consistent_read=True)
		if  current_attrs == None:
			attrs = {'': 0}
			user_domain.put_attributes(wallet_id, attrs)
			json_response = json.dumps({'current_balance':0})
		else:
			current_balance = current_attrs['current_balance']
			json_response = json.dumps({'current_balance':current_balance})
		return HttpResponse(json_response)

def get_clients(request): 
	if request.method == 'GET': 
		conn = aws_connect()
		business_domain = conn.get_domain('business_table')
		query = 'select * from `business_table`' 
		rs = business_domain.select(query)
		output = []
		for attrs in rs: 
			output.append(attrs['website'])	
		json_response = json.dumps(output)
		return HttpResponse(json_response)

