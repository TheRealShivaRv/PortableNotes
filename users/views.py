from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from .models import EmailVerification
from django.contrib.auth import authenticate, login, logout
from notes.models import NotesFile
import random

def index(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "You've successfully logged in!")
            return redirect('dashboard')
        else:
            messages.error(request, 'Your credentials are invalid')
            return redirect('index')
    return render(request, 'index.html')

def logoutapp(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "You've been successfully logged out!")
        return redirect('index')
    else:
        return redirect('index')

def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        context = {
            'email': email,
            'username': username,
            'password': password,
            'password2': password2
        }
        if not email:
            messages.error(request, 'Please enter your email id')
            return render(request, 'signup.html', context)
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'This email id is already registered')
            return render(request, 'signup.html', context)
        elif not username:
            messages.error(request, 'Please enter your username')
            return render(request, 'signup.html', context)
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'This username is already registered')
            return render(request, 'signup.html', context)
        elif not password:
            messages.error(request, 'Please enter your password')
            return render(request, 'signup.html', context)
        elif len(password) < 6:
            messages.error(request, 'Your password is lesser than 6 characters.')
            return render(request, 'signup.html', context)
        elif not password2:
            messages.error(request, 'Please confirm your password')
            return render(request, 'signup.html', context)
        elif password != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'signup.html', context)
        else:
            OTP = str(random.randint(123456, 999999))
            purpose = 'Account Creation'
            if EmailVerification.objects.filter(email=email,OTP=OTP,username=username,purpose=purpose).exists():
                messages.error(request, 'You have already requested for an OTP, Check your inbox!')
                return redirect('signup')
            else:
                OTPQueryModel = EmailVerification(email=email,OTP=OTP,username=username,purpose=purpose)
                OTPQueryModel.save()
                send_mail(
                    'Your Email Verification OTP',
                    'Your OTP is:-' + OTP,
                    'sanders.yorkshire.150b@gmail.com',
                    [email],
                    fail_silently=False,
                )
                context = {
                    'email': email,
                    'username': username,
                    'password': password,
                    'otp': OTP,
                }
                messages.success(request, 'Your One Time Password is sent to your email inbox!')
                return render(request, 'verification.html', context)

    return render(request, 'signup.html')

def resetpwd(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            OTP = str(random.randint(111111,999999))
            user = User.objects.get(email=email)
            username = user.username
            purpose = 'Password Reset'
            OTPQueryModel = EmailVerification(email=email,OTP=OTP,username=username,purpose=purpose)
            OTPQueryModel.save()
            send_mail(
                'Your Email Verification OTP',
                'Your OTP is:-' + OTP,
                'sanders.yorkshire.150b@gmail.com',
                [email],
                fail_silently=False,
            )
            context = {
                'email': email,
                'otp': OTP,
            }
            messages.success(request, 'Your One Time Password is sent to your email inbox!')
            return render(request, 'pwdresetverification.html', context)
        else:
            messages.error(request, 'This email id is not registered with us')
    return render(request, 'resetpwd.html')
def pwdresetverification(request):
    if request.method == 'POST':
        OTPinput = request.POST['otp']
        email = request.POST['email']
        if EmailVerification.objects.filter(email=email, OTP=OTPinput).exists():
            query = EmailVerification.objects.get(email=email, OTP=OTPinput)
            context = {
                'email': email,
            }
            messages.success(request, 'OTP Confirmation successful, please enter your new password')
            return render(request, 'passwordreset.html', context)
def passwordreset(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if len(password) >= 6:
            if password == password2:
                user = User.objects.get(email=email)
                user.set_password(password)
                user.save()
                messages.success(request, 'Password reset successful')
                return redirect('index')
def verification(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        otp = request.POST['otp']
        if EmailVerification.objects.filter(email=email,OTP=otp).exists():
            User.objects.create_user(email=email, username=username, password=password)
            OTPQuery = EmailVerification.objects.get(email=email,OTP=otp)
            OTPQuery.delete()
            messages.success(request, 'We have created your account, Please login to continue')
            return redirect('index')
    return render(request, 'verification.html')

def settings(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            currentemail = request.POST['currentemail']
            currentusername = request.POST['currentusername']
            currentpassword = request.POST['currentpassword']
            confirmpassword = request.POST['confirmpassword']
            if len(currentpassword) >= 6:
                if currentpassword == confirmpassword:
                    user = User.objects.get(username=request.user.username)
                    user.username = currentusername
                    user.email = currentemail
                    user.set_password(currentpassword)
                    user.save()
                    logout(request)
                    messages.success(request, 'Your credentials has been updated!')
                    return redirect('index')
                else:
                    messages.error(request, "Passwords didn't match")
            else:
                messages.error(request, 'The length of the password is less than 6 characters')
                return redirect('settings')
        else:
            return redirect('index')

    return render(request,'settings.html')
def deleteuser(request):
    if request.method == 'POST':
        username = request.POST['username']
        userdata = NotesFile.objects.filter(username=username)
        userdata.delete()
        user = User.objects.get(username=username)
        user.delete()
        messages.success(request, 'Your account has been deleted, Goodbye! :)')
        return redirect('index')
