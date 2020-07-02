#from django.contrib import admin
from django.urls import path,include
from .views import CourseListView,CourseDetailView,my_course_list_view

app_name='courses'

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('',CourseListView.as_view(),name='courselist'),
    path('<int:pk>',CourseDetailView.as_view(),name='courseDetail'),
    path('my_course_list',my_course_list_view,name='purchased_course_list'),
]