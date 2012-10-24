from django.conf.urls import patterns, include, url


urlpatterns = patterns('accounts.views',
	url(r'^$', 'login'),                    # /
	url(r'^register/$', 'register'),        # /register/
	url(r'^profile/$', 'profile'),        	# /profile/
	url(r'^profile/password/$', 'password'),# /profile/password/
	url(r'^profile/update/$', 'update'),    # /profile/update/
	url(r'^logout/$', 'logout'),            # /logout/
)
