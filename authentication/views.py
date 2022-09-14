from http.client import HTTPResponse
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from chiton import settings 
from django.core.mail import send_mail
# Create your views here.
def home(request):
     return render(request, "authentication/index.html")

def signup(request):

    if request.method == "POST":
        username = request.POST['first_name']
        sname = request.POST['second_name']
        email = request.POST['email']
        pass1 = request.POST['password']
        
        if User.objects.filter(username=username):
            messages.error(request, "Username already exists, please try another")
        if User.objects.filter(email = email):
            messages.error(request, "Email already registered ")
            return redirect('home')
        if len(username)>10:
            messages.error(request, "Username must be under 10 characters")




        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = username
        myuser.second_name = sname
        
        myuser.save()

        messages.success(request, "Your account has been successfully created.")
        #welcome email

        subject = "Welcome to Chiton-Django Login"
        message = "Hello " + myuser.first_name + " \n" + "Welcome to chiton \n Thank you for visitingnnour website \n We have also sent you a confirmation email, please check your inbox"
        from_mail = settings.EMAIL_HOST_USER 
        to_list = [myuser.email]
        send_mail(subject, message, from_mail, to_list, fail_silently=True)
        return redirect('signin')

    return render(request, "authentication/signup.html")



def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['passcode']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.username
            return render(request, "authentication/index.html", {'fname': username})
            
        else:
            messages.error(request, "Bad credentials")
            return redirect('home')
    return render(request, "authentication/signin.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged Out sucessfully")
    return redirect('home')

    


    
