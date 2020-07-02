from __future__ import print_function

from django.shortcuts import render,reverse,redirect
import stripe
from django.views import View
from .models import Payment
from django.contrib.auth.mixins import LoginRequiredMixin
from courses.models import CourseTransactions,Course
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required

#Google Drive API imports


from django.shortcuts import render
from django.http import HttpResponse
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient import discovery
import httplib2
from . import auth
#import json
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

CLIENT_SECRET_FILE = 'credentials.json'
APPLICATION_NAME = 'Quickstart'
authInst = auth.auth(SCOPES,CLIENT_SECRET_FILE,APPLICATION_NAME)
credentials = authInst.getCredentials()

http = credentials.authorize(httplib2.Http())

from apiclient import errors
# ...

drive_service = discovery.build('drive', 'v3', http=http)

stripe.api_key = 'sk_test_lZsEGIiefv9IAuUSDTCcw9xd00CUURH4F7'

course_and_folder_id={
    'Course-1':'1Y9NuGBLyqP94nwpCn_k0ICad8uK6Z87E',
    'Course-2':'1g3nAGNRiHSH5QgxWoa8wrCHTI7cPwkQj',
    'Course-3':'1TjPTkW3a0PL1I5BdyapK6BjwezFYWYl1'
}
# Create your views here.

'''class PaymentView(LoginRequiredMixin,View):
    login_url = '/login/'

    def get(self,request,pk,*args,**kwargs):
        C=Course.objects.filter(pk=pk)
        #return redirect(reverse('payments',kwargs={'pk':pk}))
        #html_file=f"payments/payments.html/{pk}"
        #return render(self.request,html_file,{'course_selected':C})

        #Few mistakes that I did are commented above

        return render(self.request,"payments/payments.html",{'course_selected':C})

    def post(self,pk,*args,**kwargs):
        token=self.request.POST.get('stripeToken')
        charge = stripe.Charge.create(
            amount=20,
            shipping={
                'name': 'Jenny Rosen',
                'address': {
                    'line1': '510 Townsend St',
                    'postal_code': '98140',
                    'city': 'San Francisco',
                    'state': 'CA',
                    'country': 'US',
                }
            },
            currency='usd',
            description="Testing",
            source=token,
        )
        print(request.POST.get('course_selected'))
        #ct=CourseTransactions(course_name=,user_name=self.request.user)
        #ct.save()

        return render(self.request,"courses/my_course_list.html")

        pymnt=Payment()
        pymnt.stripe_charge_id=charge['id']
        pymnt.user=self.request.user
        pymnt.amount=20.00
        pymnt.save()

    #return render(request,'payments/first.html')'''

@login_required
def PaymentView(request,pk):
    if request.method=='POST':
        token=request.POST.get('stripeToken')
        charge = stripe.Charge.create(
            amount=20,
            shipping={
                'name': 'Jenny Rosen',
                'address': {
                    'line1': '510 Townsend St',
                    'postal_code': '98140',
                    'city': 'San Francisco',
                    'state': 'CA',
                    'country': 'US',
                }
            },
            currency='usd',
            description="Testing",
            source=token,
        )
        print(request.POST.get('course_selected'))
        return render(request,"courses/my_course_list.html")
    else:
        C=Course.objects.filter(pk=pk)
        # ***** rememer C is query set,to get the object use C[0]
        #print(C[0].price)
        #print(type(C[0].price))
        return render(request,"payments/payments.html",{'course_selected':C[0]})

@login_required
def chargeView(request):
    if request.method=='POST':
        #print("post")
        course_selected=request.POST.get('course_selected')
        course_selected_price=request.POST.get('course_selected_price')
        token=request.POST.get('stripeToken')
        #print(course_selected)
        #print(type(course_selected_price))
        #print(f"willl gettt printed herereee {course_selected_price}")
        #print(type(int(course_selected_price)))
        charge = stripe.Charge.create(
            amount=int(course_selected_price),
            shipping={
                'name': request.user.username,
                'address': {
                    'line1': '510 Townsend St',
                    'postal_code': '98140',
                    'city': 'San Francisco',
                   'state': 'CA',
                    'country': 'US',
                }
            },
            currency='usd',
            description="Testing",
            source=token,
        )
        #print(request.POST.get('course_selected'))
        #return render(request,"courses/my_course_list.html")
        #print(course_selected)
        course_obj=Course.objects.filter(course_name=course_selected,price=course_selected_price)
        pymnt=Payment()
        pymnt.stripe_charge_id=charge['id']
        pymnt.user=request.user
        pymnt.course_name=course_obj[0]   #since its a query set
        pymnt.amount=int(course_selected_price)
        pymnt.save()

        course_transaction_entry=CourseTransactions(course_name=course_obj[0],user_name=request.user)
        course_transaction_entry.save()

        insert_permission(drive_service,course_and_folder_id.get(course_selected),request.user.email,'user','reader')

        ct_qs=CourseTransactions.objects.filter(user_name=request.user)
        return render(request,'courses/my_course_list.html',{'course_list':ct_qs})

    else:
        ct_qs=CourseTransactions.objects.filter(user_name=request.user)
        return render(request,'courses/my_course_list.html',{'course_list':ct_qs})
        #my mistake return render(request,"courses/my_course_list.html",{})


#Google drive API insert permission code


def insert_permission(service, file_id, value, perm_type, role):
  """Insert a new permission.

  Args:
    service: Drive API service instance.
    file_id: ID of the file to insert permission for.
    value: User or group e-mail address, domain name or None for 'default'
           type.
    perm_type: The value 'user', 'group', 'domain' or 'default'.
    role: The value 'owner', 'writer' or 'reader'.
  Returns:
    The inserted permission if successful, None otherwise.
  """
  new_permission = {
      #'value': value,
      'type': perm_type,
      'role': role,
      'emailAddress': value
  }
  try:
    return service.permissions().create(
        fileId=file_id, body=new_permission).execute()
  except errors.HttpError as error:             #errors.HttpError,
    print ('An error occurred: %s' %( error))
  return None

