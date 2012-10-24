from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Survey(models.Model):
	user = models.ForeignKey(User)
	description = models.CharField(max_length=200)
	pub_date = models.DateTimeField(auto_now_add=True)
	mod_date = models.DateTimeField(auto_now=True)
	
	def __unicode__(self):
		return self.description
	

class Question(models.Model):
	QUESTION_CHOICES = (
		('RB','Radio Button'),
		('CB','Check Box'),
		('TF','Text Field'),
		('NI','Numeric Input'),
	)
	
	survey = models.ForeignKey(Survey)
	description = models.CharField(max_length=200)
	questionno = models.IntegerField()
	questiontype = models.CharField(max_length=2, choices=QUESTION_CHOICES)
	
	class Meta:
		ordering = ['questionno']
	
	def __unicode__(self):
		return self.description


class Choice(models.Model):
	question = models.ForeignKey(Question)
	description = models.CharField(max_length=50, null=True)
	votes = models.IntegerField(null=True)
	choiceno = models.IntegerField(null=True)
	
	class Meta:
		ordering = ['choiceno']
	
	def __unicode__(self):
		return self.description
		
class Response(models.Model):
	survey = models.ForeignKey(Survey)
	responsetime = models.IntegerField(default=0)
	ipaddress = models.CharField(max_length=50, null=True)
	valid = models.BooleanField(default=False)
	accessdate = models.DateTimeField(auto_now_add=True)
	
	def __unicode__(self):
		return self.description
