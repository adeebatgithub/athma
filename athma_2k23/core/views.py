from django.shortcuts import render, redirect
from django.views import View
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from . import models
#from django.http import HttpResponse

# Create your views here.


def index(request):
    ctx = {
        "user": request.user
    }
    return render(request, 'index.html', ctx)

class LoginView(View):

    def get(self,request):
        return render(request, "login.html")

    def post(self,request):
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        print(f"\n\t {user} \n")
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            return render(request, "login.html",{"error":"somthing went wrong"})

def LogoutView(request):
    auth.logout(request)
    return redirect('/')

class SignupView(View):

    def get(self,request):
        return render(request, "signup.html")

    def post(self,request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = auth.authenticate(username=username, password=raw_password)
            auth.login(request, user)
            return redirect('profiledit')
        else:
            return render(request, "signup.html", {"form": UserCreationForm()})

class ProfileView(View):
    #@login_required
    def get(self, request):
        profile = models.Profiles.objects.get(user=request.user)
        ctx = {
            "profile": profile,
        }
        return render(request,'profile.html',ctx)

    def post(self,request):
        return redirect('profiledit')

class ProfileAdd(View):

    def get(self, request):
        return render(request, 'profile_edit.html', ctx)

    def post(self, request):
        fullname = request.POST['username']
        branch = request.POST['dept']
        semester = request.POST['sem']
        phone = request.POST['phone']

        profile = models.Profiles(fullname=fullname, branch=branch, semester=semester, phone=phone)
        profile.save()
        return redirect('profile')

class ProfileEdit(View):

    def get(self, request):
        profile = models.Profiles.objects.get(user=request.user)
        ctx = {
            "profile": profile
        }
        return render(request,'profile_edit.html',ctx)

    def post(self, request):

        fullname = request.POST['username']
        email = request.POST['email']
        branch = request.POST['dept']
        semester = request.POST['sem']
        phone = request.POST['phone']

        print(f"\n\t {request.user} \n")

        profile = models.Profiles.objects.get(user=request.user)
        profile.fullname = fullname
        profile.user.email = email
        profile.branch = branch
        profile.semester = semester
        profile.phone = phone
        profile.save()

        print("\n\t post save \n")

        return redirect('profile')
