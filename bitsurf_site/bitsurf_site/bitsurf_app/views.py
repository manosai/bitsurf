# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

def home(request):
    return render_to_response('', {}, RequestContext(request))