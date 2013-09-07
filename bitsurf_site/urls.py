from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'bitsurf_app.views.home'), 
	url(r'^login/', 'bitsurf_app.views.get_user'), 
	url(r'^check-site/', 'bitsurf_app.views.get_clients')
	url(r'^send-payment/', 'bitsurf_app.views.send_payment')
)

