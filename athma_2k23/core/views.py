from django.shortcuts import render, redirect
from django.views import View
from django.contrib import auth
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
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password_cfrm = request.POST["password_cfrm"]

        if password_cfrm == password:
            user = models.User(username=username, email=email)
            user.set_password(password)
            user.save()
            auth.authenticate(username=username, password=password)
            auth.login(request, user)
            profile = models.Profiles(user=user)
            profile.save()

            return redirect('profiledit')

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

        profile = models.Profiles.objects.get(user=request.user)
        profile.fullname = fullname
        profile.user.email = email
        profile.branch = branch
        profile.semester = semester
        profile.phone = phone
        profile.save()

        return redirect('profile')
