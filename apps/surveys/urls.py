from django.conf.urls import patterns, include, url



urlpatterns = patterns('surveys.views',
	url(r'^home/$', 'home'),															# /surveys/home/
	url(r'^create/$', 'create'),														# /surveys/create/
	url(r'^(?P<survey_id>\d+)/newquestion/$', 'newQuestion'),							# /surveys/<survey_id>/newquestion/
	url(r'^(?P<survey_id>\d+)/editquestion/(?P<question_no>\d+)/$', 'editQuestion'), 	# /surveys/<survey_id>/editquestion/<question_id>/
	# url(r'^(?P<survey_id>\d+)/view/$', 'view'),										# /surveys/<survey_id>/view/
	url(r'^(?P<survey_id>\d+)/edit/$', 'edit'),											# /surveys/<survey_id>/edit/
	url(r'^(?P<survey_id>\d+)/delete/$', 'deleteSurvey'),								# /surveys/<survey_id>/delete/
	url(r'^(?P<survey_id>\d+)/deletequestion/(?P<question_no>\d+)/$', 'deleteQuestion'),# /surveys/<survey_id>/deletequestion/<question_id>/
	url(r'^(?P<survey_id>\d+)/$', 'attempt'),											# /surveys/<survey_id>/
	url(r'^completed/$', 'completed'),                                                  # /surveys/completed/
	url(r'^(?P<survey_id>\d+)/reset/$', 'reset'),										# /surveys.<survey_id>/reset/
	)

