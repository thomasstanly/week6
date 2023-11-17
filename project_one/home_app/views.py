from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import cache_control
from admin_app.views import admin_home_page

# user login page function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login_page(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect(admin_home_page)
        return redirect(home_page)
    if request.method == "POST":
        user = request.POST["username"]
        passw = request.POST["password"]
        user_details = authenticate(username=user,password=passw)
        if user_details is not None and user_details.is_superuser is False:
            request.session['username'] = user
            login(request,user_details)
            return redirect(home_page)
        else:
            messages.warning(request,"invalid credentials")
            return redirect(login_page)

    return render(request,'user/main_login.html')

# user signup page function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signup_page(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect(admin_home_page)
        return redirect(home_page)
    if request.method == "POST":
        user = request.POST["username"]
        passw = request.POST["password"]
        conpass = request.POST["confirm_password"]
        try:
                if User.objects.get(username = user):
                    messages.warning(request,"username  is taken")
                    return redirect(signup_page)
        except:
                pass
        if passw != conpass:
            messages.warning(request,"Password is incorrect")
            return redirect(signup_page)
        if len(passw) < 8:
            messages.info(request,"Password minimum 8 characters")
            return redirect(signup_page)
        user_details = User.objects.create_user(username = user,password = passw)
        user_details.save()
        return redirect(login_page)

    return render(request,'user/main_signup.html')

# user hone page page function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home_page(request):
    if request.user.is_authenticated:
        return render(request,'user/main_home.html')
    
    return redirect(login_page)

    
def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
    messages.success(request,'logout successfully')
    return redirect(login_page)