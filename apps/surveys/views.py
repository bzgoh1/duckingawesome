from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, time, date, timedelta
from accounts.models import UserProfile
from .models import Survey, Question, Choice, Response
from .forms import *


# Create your views here.

@login_required
def home(request):
	surveyList = Survey.objects.filter(user=request.user)
	for survey in surveyList:
		for response in survey.response_set.all():
			if response.valid == False:
				response.delete()
	urllink = request.build_absolute_uri()
	urllink = str.replace(urllink, 'home/', '')
	return render(request, 'surveys/home.html', {'surveyList': surveyList, 'urllink': urllink})


@login_required
def create(request):
	user = request.user
	form = SurveyForm(request.POST or None)
	
	if form.is_valid():
		survey = user.survey_set.create(description=form.cleaned_data['description'])		
		
		return redirect('surveys.views.newQuestion', survey_id=survey.id )
		
	return render(request, 'surveys/create.html', {'form': form})

	
@login_required
@csrf_exempt
def newQuestion(request, survey_id):
	user = request.user
	form = QuestionForm(request.POST or None)
	try:
		survey = user.survey_set.get(pk=survey_id)
	except Survey.DoesNotExist:
		raise Http404
	
	if form.is_valid():
		qntype = request.POST['qntype']
		qnno = 1
		while survey.question_set.filter(questionno = qnno):
			qnno += 1
		if qntype == 'CB' or qntype == 'RB':
			if form.cleaned_data['choice1'] or form.cleaned_data['choice2'] or form.cleaned_data['choice3'] or form.cleaned_data['choice4']:
				question = survey.question_set.create(description=form.cleaned_data['description'], questionno = qnno)
				question.questiontype = qntype
				question.save()
				if form.cleaned_data['choice1']:
					question.choice_set.create(description=form.cleaned_data['choice1'], votes=0, choiceno=1)
				if form.cleaned_data['choice2']:
					question.choice_set.create(description=form.cleaned_data['choice2'], votes=0, choiceno=2)
				if form.cleaned_data['choice3']:
					question.choice_set.create(description=form.cleaned_data['choice3'], votes=0, choiceno=3)
				if form.cleaned_data['choice4']:
					question.choice_set.create(description=form.cleaned_data['choice4'], votes=0, choiceno=4)
			else:
				messages.error(request, u'Please enter at least 1 choice.')
		else:
			question = survey.question_set.create(description=form.cleaned_data['description'], questionno = qnno)
			question.questiontype = qntype
			question.save()
			survey.save()

	return render(request, 'surveys/newquestion.html', {'form': form, 'survey_id': survey_id, 'survey': survey,})
	
	
@login_required
@csrf_exempt
def editQuestion(request, survey_id, question_no):
	user = request.user
	
	try:
		survey = user.survey_set.get(pk=survey_id)
	except Survey.DoesNotExist:
		raise Http404

	try:
		question = survey.question_set.get(questionno=question_no)
	except Survey.DoesNotExist:
		raise Http404
		
	initial = { 'description': question.description, 'questionno': question.questionno }
	
	choicelist = ['choice1', 'choice2', 'choice3', 'choice4']
	
	choiceno = 1
	
	for ch in choicelist:
		if question.choice_set.filter(choiceno=choiceno):
			choice = question.choice_set.get(choiceno=choiceno)
			description = choice.description
			initial[ch] = description
		else:
			initial[ch] = ''
		choiceno = choiceno + 1
		
	form = QuestionForm(request.POST or None, initial = initial)
	if form.is_valid():
		qntype = request.POST['qntype']
		if qntype == 'CB' or qntype == 'RB':
			if form.cleaned_data['choice1'] or form.cleaned_data['choice2'] or form.cleaned_data['choice3'] or form.cleaned_data['choice4']:
				question.description = form.cleaned_data['description']
				question.questiontype = qntype
				question.save()
				if question.choice_set.filter(choiceno=1):
					choice = question.choice_set.get(choiceno=1)
					if form.cleaned_data['choice1']:
						choice.description = form.cleaned_data['choice1']
						choice.save()
					else:
						choice.delete()
				else:
					if form.cleaned_data['choice1']:
						question.choice_set.create(description=form.cleaned_data['choice1'], votes=0, choiceno=1)
				if question.choice_set.filter(choiceno=2):
					choice = question.choice_set.get(choiceno=2)
					if form.cleaned_data['choice2']:
						choice.description = form.cleaned_data['choice2']
						choice.save()
					else:
						choice.delete()
				else:
					if form.cleaned_data['choice2']:
						question.choice_set.create(description=form.cleaned_data['choice2'], votes=0, choiceno=2)
				if question.choice_set.filter(choiceno=2):
					choice = question.choice_set.get(choiceno=2)
					if form.cleaned_data['choice2']:
						choice.description = form.cleaned_data['choice2']
						choice.save()
					else:
						choice.delete()
				else:
					if form.cleaned_data['choice2']:
						question.choice_set.create(description=form.cleaned_data['choice2'], votes=0, choiceno=2)
				if question.choice_set.filter(choiceno=3):
					choice = question.choice_set.get(choiceno=3)
					if form.cleaned_data['choice3']:
						choice.description = form.cleaned_data['choice3']
						choice.save()
					else:
						choice.delete()
				else:
					if form.cleaned_data['choice3']:
						question.choice_set.create(description=form.cleaned_data['choice3'], votes=0, choiceno=3)
				if question.choice_set.filter(choiceno=4):
					choice = question.choice_set.get(choiceno=4)
					if form.cleaned_data['choice4']:
						choice.description = form.cleaned_data['choice4']
						choice.save()
					else:
						choice.delete()
				else:
					if form.cleaned_data['choice4']:
						question.choice_set.create(description=form.cleaned_data['choice4'], votes=0, choiceno=4)
				messages.success(request, u'Your question has been edited.')
				survey.save()
			else:
				messages.error(request, u'Please enter at least 1 choice.')
		else:
			question.description = form.cleaned_data['description']
			question.questiontype = qntype
			question.save()
			messages.success(request, u'Your question has been edited.')
			survey.save()
			
			for choice in question.choice_set.all():
				choice.delete()
				
				
		return redirect('surveys.views.editQuestion', survey_id=survey_id , question_no=question_no,)
	
	return render(request, 'surveys/question.html', {'form': form, 
		'survey_id': survey_id, 
		'initial': initial, 
		'question_no': question_no,
		'qntype': question.questiontype,
		'survey': survey,})


@login_required
@csrf_exempt
def deleteSurvey(request, survey_id):
	user = request.user
	
	try:
		survey = user.survey_set.get(pk=survey_id)
	except Survey.DoesNotExist:
		raise Http404
		
	survey.delete()
	messages.success(request, u'Your survey has been deleted.')
	
	return redirect('/surveys/home/')


@login_required
@csrf_exempt
def deleteQuestion(request, survey_id, question_no):
	user = request.user
	
	try:
		survey = user.survey_set.get(pk=survey_id)
	except Survey.DoesNotExist:
		raise Http404
	
	try:
		question = survey.question_set.get(questionno=question_no)
	except Survey.DoesNotExist:
		raise Http404
	
	qnno = int(question_no)
	qnno = qnno + 1
	
	while survey.question_set.filter(questionno = qnno):
		nextqn = survey.question_set.get(questionno = qnno)
		nextqn.questionno = nextqn.questionno - 1
		nextqn.save()
		qnno = qnno + 1
		
	question.delete()
	survey.save()
	messages.success(request, u'Your question has been deleted.')
	
	if survey.question_set.filter(questionno = question_no):
		return redirect('surveys.views.editQuestion', survey_id=survey_id, question_no=question_no)
	else:
		return redirect('surveys.views.newQuestion', survey_id=survey_id)

		
@login_required
def edit(request, survey_id):
	user = request.user
	try:
		survey = user.survey_set.get(pk=survey_id)
		initial = {'description': survey.description}
	except Survey.DoesNotExist:
		raise Http404

	form = SurveyForm(request.POST or None, initial = initial)
	
	if form.is_valid():
		survey.description = form.cleaned_data['description']
		survey.save()
		
		messages.success(request, u'Your survey title has been edited.')
		
	return render(request, 'surveys/edit.html', {'form': form, 'survey_id': survey_id, 'survey': survey})


@csrf_exempt
def attempt(request, survey_id):
	
	survey = get_object_or_404(Survey, pk=survey_id)

	if request.method == 'GET':
		start = datetime.now() - datetime.combine(date.today() - timedelta(days=1), time(0, 0))
		starttime = start.days*86400+ start.seconds
		response = survey.response_set.create(responsetime=starttime, ipaddress=request.META.get('REMOTE_ADDR'))
	
	if request.method == 'POST':
		qnno = 1
		while survey.question_set.filter(questionno=qnno):
			question = survey.question_set.get(questionno=qnno)
			qnname = 'q' + str(qnno)
			if question.questiontype == 'TF':
				try: 
					request.POST[qnname]
					question.choice_set.create(description=request.POST[qnname], votes=0, choiceno=0)
				except:
					pass
			elif  question.questiontype == 'RB':
				try: 
					request.POST[qnname]
					choice = get_object_or_404(Choice, pk=request.POST[qnname])			
					choice.votes += 1
					choice.save()
				except:
					pass
			elif question.questiontype == 'CB':
				try:
					request.POST[qnname]
					for value in request.POST[qnname]:
						choice = get_object_or_404(Choice, pk=request.POST[qnname])	
						choice.votes += 1
						choice.save()
				except:
					pass
			elif question.questiontype == 'NI':
				try: 
					request.POST[qnname]
					question.choice_set.create(description="Numberic Input", votes=int(request.POST[qnname]), choiceno=0)
				except:
					pass
			qnno = qnno + 1
		
		responses = survey.response_set.filter(survey_id=survey_id, ipaddress=request.META.get('REMOTE_ADDR'), valid=False)
		response_id = 0;
		for response in responses:
			if response.id > response_id:
				response_id = response.id
				
		response = survey.response_set.get(pk=response_id)
		response.valid = True
		end = datetime.now() - datetime.combine(date.today() - timedelta(days=1), time(0, 0))
		endtime = end.days*86400+ end.seconds
		response.responsetime = endtime-response.responsetime
		response.save()
		
		return redirect('surveys.views.completed')
					
		
	return render(request, 'surveys/attempt.html', {'survey_id': survey_id, 'survey': survey})


def completed(request):
	if request.user.is_authenticated():
		return redirect('/surveys/home/')
	else:
		return render(request, 'surveys/completed.html')

		
@login_required		
def reset(request, survey_id):
	user = request.user
	
	try:
		survey = user.survey_set.get(pk=survey_id)
	except Survey.DoesNotExist:
		raise Http404
		
	for question in survey.question_set.all():
		if question.questiontype == 'TF' or question.questiontype == 'NI':
			for choice in question.choice_set.all():
				choice.delete()
		elif question.questiontype == 'CB' or question.questiontype == 'RB':
			for choice in question.choice_set.all():
				choice.votes = 0
				choice.save()

	for response in survey.response_set.all():
		response.delete()

	messages.success(request, u'Your survey has been reset.')
	
	return redirect('/surveys/home/')











		
	
	
