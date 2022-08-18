from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from loginsys import settings
from django.core.mail import send_mail


# Create your views here.
def home(request):
    return render(request, "verification/base.html")

# Sign up
def signup(request):

    if request.method == "POST":
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')


        if User.objects.filter(username=username):
            messages.error(request, "Username already exists")
            return redirect('home')

        if User.objects.filter(email=email):
            messages.error(request, "This email is already being used by another user")
            return redirect('home')

        # if len(username)<10:
        #     messages.error(request, "Your username must not be lesser than 10 characters")


        if password1 != password2:
            messages.error(request, "Incorrect password")
            return redirect('home')




        myuser = User.objects.create_user(username, email, password1)
        myuser.first_name = fname
        myuser.last_name = lname
 
        myuser.save()

        messages.success(request, "Your account has been succesfully created!")

        # Welcome email confirmation message
  
        # subject = "Welcome to Juls_Dash"
        # message = "Hello " + myuser.first_name + myuser.last_name + "!! \n" + "Thanks for signing up to our site \n We have sent you a confirmation email, please confirm your email address in order to activate your account"
        # from_email = settings.EMAIL_HOST_USER
        # to_list = [email]
        # send_mail(subject, message, from_email, to_list, fail_silently=True)

        return redirect("signin")

    return render(request, "verification/signup.html")


# Signin
def signin(request):

    if request.method == "POST":
        username = request.POST['username']
        password1 = request.POST['password1']

        user = authenticate(username=username, password=password1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "verification/index.html", {'fname': fname})

        else:
            messages.error(request, "Invalid username or password")
            return redirect('home')

    return render(request, "verification/signin.html")

    


# Sign out
def signout(request):
    logout(request)
    messages.success(request, "Log out successful!")
    return redirect('home')