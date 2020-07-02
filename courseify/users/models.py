from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings

# Create your models here.

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    image=models.ImageField(default='profile_pics/default.jpg',upload_to='profile_pics')

def createProfile(sender,instance,created,*args,**kwargs):
    if created:
        p=Profile(user=instance)
        p.save()

post_save.connect(createProfile,sender=settings.AUTH_USER_MODEL)