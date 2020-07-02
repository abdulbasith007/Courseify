from django.db import models
from django.conf import settings
# Create your models here.

class Course(models.Model):
    course_name=models.CharField(max_length=20)
    description=models.CharField(max_length=50)
    price=models.IntegerField(default=0)

    def __str__(self):
        return self.course_name

    @property
    def lessons(self):
        return self.lesson_set.all().order_by('position')

class CourseTransactions(models.Model):
    course_name=models.ForeignKey(Course,on_delete=models.CASCADE)
    user_name=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

class Lesson(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    lesson_name=models.CharField(max_length=20)
    position=models.IntegerField()
    video_url=models.CharField(max_length=50)
    thumbnail=models.ImageField(null=True)

    def __str__(self):
        return self.lesson_name