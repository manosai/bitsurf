import json
import os
import requests

from django.http import HttpResponse, HttpResponseRedirect
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
		bitcoin_address = str(request.GET['bitcoin_addr'])
		current_attrs = user_domain.get_item(bitcoin_address, consistent_read=True)
		if  current_attrs == None:
			attrs = {'total_earned':0}
			user_domain.put_attributes(bitcoin_address, attrs)
			json_response = json.dumps(attrs)
		else:
			total_earned = current_attrs['total_earned']
			json_response = json.dumps({'total_earned':total_earned})
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
			website = attrs.name
			output[website] = attrs['rate']
        json_response = json.dumps(output)
        return HttpResponse(json_response)

# Update user balance and call send_payment
def update_balance(request):
	if request.method == 'GET': 
		conn = aws_connect()
		bitcoin_address = request.GET["bitcoin_addr"]
		website = request.GET["website"]

		# lookup website's payout rate
		business_domain = conn.get_domain('business_table')
		curr_business = business_domain.get_item(website, consistent_read=True)
		amount = float(curr_business['rate'])

		# check for sufficient funds
		funds = float(curr_business['funds'])
		if funds < amount: 
			return HttpResponse('<h1>The company no longer has enough funds to pay you.</h1>')

		return send_payment(bitcoin_address, amount)

# Send payment via Coinbase API
def send_payment(bitcoin_address, amount):
	conn = aws_connect()
	transaction_dic = {}
	account = CoinbaseAccount(api_key=os.environ['coinbase_api_key'])
	transaction = account.send(bitcoin_address, amount)
	transaction_dic['transaction_status'] = str(transaction.status)
	
	# add to user's balance 
	user_domain = conn.get_domain('user_table')
	user = user_domain.get_item(bitcoin_address, consistent_read=True)
	user['total_earned'] = str(float(user['total_earned']) + amount)
	user.save()
	
	transaction_dic['total_earned'] = user['total_earned']
	json_response = json.dumps(transaction_dic)

	return HttpResponse(json_response)

def business_register(request):
	if request.method == 'POST':
		website = request.POST['website']
		conn = aws_connect()
		business_domain = conn.get_domain('business_table')
		bus_attrs = business_domain.get_item(website, consistent_read=True)
		if bus_attrs != None:
			return render_to_response('', {}, RequestContext(request))
		else:
			bus_attrs = {'rate':request.POST['rate']}
			business_domain.put_attributes(website, bus_attrs)
			return HttpResponseRedirect("https://coinbase.com/checkouts/321d8ede9082981b1ea1c79cd261d66d")

def business_home(request):
	if request.method == 'GET':

		return render_to_response('admin_home.html', {'website': website, \
			'funds':funds, 'rate':rate}, RequestContext(request))



