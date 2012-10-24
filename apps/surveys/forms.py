from django import forms

# Create your forms here.

class SurveyForm(forms.Form):
	description = forms.CharField(max_length=200)
	

class QuestionForm(forms.Form):
	description = forms.CharField(max_length=200)
	
	choice1 = forms.CharField(max_length=200, required=False)
	choice2 = forms.CharField(max_length=200, required=False)
	choice3 = forms.CharField(max_length=200, required=False)
	choice4 = forms.CharField(max_length=200, required=False)