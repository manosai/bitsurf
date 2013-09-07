# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

import boto.sdb.connection.SDBConnection as SDBConnection
import json

def home(request):
    return render_to_response('login.html', {}, RequestContext(request))

def add_user(request):
	if request.method == 'GET':
		conn = SDBConnection(aws_acces_key_id=, aws_secret_access_key=)
		user_domain = conn.get_domain('user_table')
		bitcoin_address = request['bitcoin_address']
		current_attrs = user_domain.get_item(bitcoin_address, consistent_read=True)
		if  current_attrs == None:
			attrs = {'': 0}
			user_domain.put_attributes(wallet_id, attrs)
			json_response = json.dumps({'current_balance':0})
		else:
			current_balance = current_attrs['current_balance']
			json_response = json.dumps({'current_balance':current_balance})
		return HttpResponse(json_response)

