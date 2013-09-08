from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'bitsurf_app.views.home'), 
	url(r'^login/', 'bitsurf_app.views.get_user'), 
	url(r'^user-register/', 'bitsurf_app.views.add_user'),
	url(r'^check-site/', 'bitsurf_app.views.get_clients'), 
	url(r'^send-payment/', 'bitsurf_app.views.update_balance'),
	url(r'^business-register/', 'bitsurf_app.views.business_register'),
	url(r'^admin/', 'bitsurf_app.views.business_home')
)

