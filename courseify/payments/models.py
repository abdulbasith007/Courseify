from django.db import models
from django.conf import settings
from courses.models import Course
# Create your models here.

class Payment(models.Model):
    stripe_charge_id=models.CharField(max_length=50)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,blank=True,null=True)
    course_name=models.ForeignKey(Course,on_delete=models.SET_NULL,null=True)
    amount=models.FloatField()
    timestamp=models.DateTimeField(auto_now_add=True)