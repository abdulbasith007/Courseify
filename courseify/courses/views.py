from django.shortcuts import render
from django.views.generic import ListView,DetailView,View
from .models import Course,CourseTransactions

# Create your views here.

class CourseListView(ListView):
    model=Course

class CourseDetailView(View):
    def get(self,request,pk,*args,**kwargs):
        course_qs=Course.objects.filter(pk=pk)
        context={'object':course_qs[0]}
        if request.user.is_authenticated:
            ct_qs=CourseTransactions.objects.filter(course_name=course_qs[0]).filter(user_name=request.user)
            context['purchased_this']=ct_qs.exists()
        
        #print(ct_qs)
        return render(request,"courses/course_detail.html",context)

def my_course_list_view(request):
    ct_qs=CourseTransactions.objects.filter(user_name=request.user)
    return render(request,'courses/my_course_list.html',{'course_list':ct_qs})