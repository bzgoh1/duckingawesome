from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as lgin, logout as lgout
from django.contrib import messages
from .models import UserProfile
from .forms import *


def login(request):
	#Added this so that logged in user will not go to log in page.
	if request.user.is_authenticated():
			return redirect('/surveys/home')

	else:
			
		form = LoginForm(request.POST or None)

		if form.is_valid():
				usernm = form.cleaned_data['username']
				passwd = form.cleaned_data['password']

				user = authenticate(username=usernm, password=passwd)

				if user and user.is_active:
						lgin(request, user)
						#Changed redirect to profile page
						return redirect('/surveys/home')
	
				else:
						messages.error(request, u'Incorrect username or password.')
		
	return render(request, 'accounts/login.html', {'form': form, })


def register(request):
	if request.user.is_authenticated():
			return redirect('/surveys/home')
	
	else:

		form = RegisterForm(request.POST or None)
		
		if form.is_valid():
		
			usernm = form.cleaned_data['username']
			
			try:
				
				user = User.objects.get(username=usernm)
				
			except User.DoesNotExist:
			
				user = None
				
			if user is None:
		
				passwd = form.cleaned_data['password']
				email = form.cleaned_data['email']
				name = form.cleaned_data['name']
				user = User.objects.create_user(
					username=usernm,  
					email=email,
					password=passwd,
				)
				user.first_name = name 
				user.save()
				
				user.get_profile().contactno = form.cleaned_data['contactno']
				user.get_profile().birthdate = form.cleaned_data['birthdate']
				user.get_profile().gender = form.cleaned_data['gender']
				user.get_profile().save()
				
				user = authenticate(username=usernm, password=passwd)
				lgin(request, user)
				return redirect('/surveys/home')
				
			else:
				messages.error(request, u'Username is already taken.')
			
	return render(request, 'accounts/register.html', {'form': form, })

	
@login_required
def profile(request):
	user = request.user
	profile = user.get_profile()
	
	return render(request, 'accounts/profile.html', {'user': user, 'profile': profile})

@login_required
def update(request):
	user = request.user
	profile = user.get_profile()
	initial = {
		'name': user.first_name,
		'email': user.email,
		'gender': profile.gender,
		'birthdate': profile.birthdate,
		'contactno': profile.contactno,
	}
	
	form = UpdateForm(request.POST or None, initial = initial)
	
	if form.is_valid():
		user.first_name =  form.cleaned_data['name']
		user.email =  form.cleaned_data['email']
		
		user.save()
		
		profile.contactno = form.cleaned_data['contactno']
		profile.birthdate = form.cleaned_data['birthdate']
		profile.gender = form.cleaned_data['gender']
		profile.save()
		
		messages.success(request, u'Your profile have been updated.')
		
		return redirect('/profile')		
		
	return render(request, 'accounts/update.html', {'form': form, })


@login_required
def password(request):
	user = request.user
	
	form = PasswordForm(request.POST or None)
	
	if form.is_valid():
		if user.check_password(form.cleaned_data['oldpassword']):
			user.set_password(form.cleaned_data['password'])
			user.save()
			messages.success(request, u'Your password has been changed.')
			return redirect('/profile')
			
		else:
			messages.error(request, u'The old password you entered is incorrect.')
			
	
	return render(request, 'accounts/password.html', {'form': form, })	
	

@login_required	
def logout(request):
        lgout(request)
        return redirect('/')
