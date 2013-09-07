import json
import os
import requests

from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
import boto.sdb
from coinbase import CoinbaseAccount

def aws_connect():
	conn = boto.sdb.connect_to_region('us-west-1',\
		aws_access_key_id=os.environ['aws_access_key_id'], \
		aws_secret_access_key=os.environ['aws_secret_access_key'])
	return conn

def home(request):
    return render_to_response('login.html', {}, RequestContext(request))

# Existing user sign in
def get_user(request):
	if request.method == 'GET':
		conn = aws_connect()
		user_domain = conn.get_domain('user_table')
		bitcoin_address = request.GET['bitcoin_addr']
		current_attrs = user_domain.get_item(bitcoin_address, consistent_read=True)
		if  current_attrs == None:
			attrs = {'current_balance': 0, 'total_earned':0}
			user_domain.put_attributes(bitcoin_address, attrs)
			json_response = json.dumps(attrs)
		else:
			current_balance = current_attrs['current_balance']
			json_response = json.dumps({'current_balance':current_balance})
		return HttpResponse(json_response)

# New user signup
def add_user(request):
	if request.method == 'GET':
		post_data = {}
		post_data["user"] = {"email":request.GET['email'], \
			"password":request.GET['password']}
		r = requests.post("https://coinbase.com/api/v1/users", data=post_data)
		json_response = json.dumps({"success": r.json()['success']})
		return HttpResponse(json_response)

# Return list of all clients
def get_clients(request):
    if request.method == 'GET':
        conn = aws_connect()
        business_domain = conn.get_domain('business_table')
        query = 'select * from `business_table`'
        rs = business_domain.select(query)
        output = {}
        for attrs in rs:
            link = attrs['website']
            output[link] = attrs['rate']
        json_response = json.dumps(output)
        return HttpResponse(json_response)

def send_payment(request):
	if request.method == 'GET':
		conn = aws_connect()
		transaction_dic = {}
		bitcoin_address = request.GET["bitcoin_addr"]
		amount = request.GET["amount"]
		account = CoinbaseAccount(api_key=os.environ['coinbase_api_key'])
		transaction = account.send(bitcoin_address, float(amount))
		json_response = json.dumps({"transaction_status":str(transaction.status)})
		user_domain = conn.get_domain('user_table')
		user = user_domain.get_item(bitcoin_address, consistent_read=True)
		user['total_earned'] = str(float(user['total_earned']) + float(transaction_amount))
		user['current_balance'] = str(float(user['current_balance']) - float(transaction_amount))
		user.save()
		return HttpResponse(json_response)



