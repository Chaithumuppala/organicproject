from django.shortcuts import render
from django.shortcuts import redirect

# Create your views here.
def signin(request):
    return render(request,"Authentication/signin.html")

def signup(request):
    print('iam running the signup view')
    return render(request,"Authentication/signup.html")

def login(request):
    return render(request,"Authentication/login.html")

def logout(request):
    return redirect('/auth/login')