from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.
class UserProfile(models.Model):
    
    user =  models.OneToOneField(User)

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    contactno = models.IntegerField(null=True, blank=False)
    birthdate = models.DateField(null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __unicode__(self):
        return self.user.username

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
