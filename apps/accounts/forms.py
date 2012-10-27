from django import forms
from django.forms import extras


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(forms.Form):	
	name = forms.CharField(max_length=30)
	username = forms.CharField(max_length=30)
	password = forms.CharField(
		widget=forms.PasswordInput, 
		label=u'Create a password'
	)
	password2 = forms.CharField(
		widget=forms.PasswordInput,
		label=u'Re-enter password'
	)
	email = forms.EmailField()
	gender = forms.ChoiceField(
		widget=forms.Select, 
		choices=[('M', 'Male'), ('F', 'Female')]
	)
	birthdate = forms.DateField(widget=extras.SelectDateWidget(years=range(1950,2013)))
	contactno = forms.IntegerField(
		label=u'Phone number', 
		required=False
	)
	
	def clean_password2(self):
		password = self.cleaned_data.get("password", "")
		password2 = self.cleaned_data["password2"]
		
		if password != password2:
			raise forms.ValidationError("The two password didn't match.")
		return password2

		
class UpdateForm(forms.Form):
	name = forms.CharField(max_length=30)
	email = forms.EmailField()
	gender = forms.ChoiceField(
		widget=forms.Select, 
		choices=[('M', 'Male'), ('F', 'Female')]
	)
	birthdate = forms.DateField(widget=extras.SelectDateWidget(years=range(1950,2013)))
	contactno = forms.IntegerField(
		label=u'Phone number', 
		required=False
	)
	
	
class PasswordForm(forms.Form):
	oldpassword = forms.CharField(
		widget=forms.PasswordInput, 
		label=u'Enter old password'
	)
	password = forms.CharField(
		widget=forms.PasswordInput, 
		label=u'Enter new password'
	)
	password2 = forms.CharField(
		widget=forms.PasswordInput,
		label=u'Re-enter new password'
	)
	
	def clean_password2(self):
		password = self.cleaned_data.get("password", "")
		password2 = self.cleaned_data["password2"]
		
		if password != password2:
			raise forms.ValidationError("The two password didn't match.")
		return password2
	
    
