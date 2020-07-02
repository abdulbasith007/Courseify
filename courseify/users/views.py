from django.shortcuts import render,redirect
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm
#We're using userCreationForm(customized) to register a user

from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

def Register(request):
    if request.method=='POST':
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request,"You're Account Has Been Created....")
            return redirect('/login/')    #/ has to be appended at the beginning,I dont know why url names arent working
    else:
        form=UserRegisterForm()
    return render(request,'users/register.html',{'form':form})

@login_required(login_url='/login/')
def ProfileView(request):
    if request.method=="POST":
        u_form=UserUpdateForm(request.POST,instance=request.user)
        p_form=ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,"Successfully Updated")
            return redirect('profile')
    else:
        u_form=UserUpdateForm()
        p_form=ProfileUpdateForm()
    return render(request,'users/profile.html',{'u_form':u_form,'p_form':p_form})