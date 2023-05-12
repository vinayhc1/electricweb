from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import AnonymousUser

# Create your views here.

def handlelogin(request):
    if request.method=='POST':
      username = request.POST['userid']
      password = request.POST['pass1']
      user = authenticate(request, username=username, password=password)
      if user is not None:
         login(request, user)
         return redirect('/home')
      else:
         messages.error(request,"Invalid Credentials")
        # return render(request, "authentication/login.html")
         return redirect('/')
    return render(request, "authentication/login.html")

def handlelogout(request):
    logout(request)
    request.session.flush()
    if hasattr(request, 'user'):
     request.user = AnonymousUser()
    return redirect('/')