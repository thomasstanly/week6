from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.views.decorators.cache import cache_control
from django.db.models import Q




# Create your views here.

# admin login page function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_log_page(request): 
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect(admin_home_page)
        return redirect(admin_home_page)
    if request.method == "POST":
        user = request.POST["admin_username"]
        passw = request.POST["admin_password"]
        user_details = authenticate(email=user,password=passw)
        if user_details is not None and user_details.is_superuser:
            request.session['username'] = user
            login(request,user_details)
            return redirect(admin_home_page)
        else:
            messages.error(request,"invalid username or password")
            return redirect(admin_log_page)
    
    return render(request,'admin/admin_log.html')


# admin home page function
def admin_home_page(request):
    if 'username' not in  request.session:
        return redirect(admin_log_page)
    user = User.objects.all().order_by('id')
    return render(request,'admin/admin_home.html',{ 'users' : user})

# logout
def admin_logout(request):
    if 'username' in request.session:
        request.session.flush()
        logout(request)
    messages.success(request,'logout successfully')
    return redirect(admin_log_page)

# creating a user
def admin_create(request):
    if request.method == 'POST' and request.user.is_superuser:
        user = request.POST['username']
        email = request.POST['user_email']
        password = request.POST['password']
        conf_password = request.POST['confirm_password']

        try:
            if User.objects.get(username = user):
                messages.warning(request,"username is taken")
                return redirect(admin_home_page)
        except:  
                pass
        try:
            if User.objects.get(email = email):
                messages.warning(request,"email is taken")
                return redirect(admin_home_page)
        except:  
                pass
        
        if password != conf_password:
            messages.warning(request,"Password doesn't match")
            return redirect(admin_home_page)
        if len(password) < 8:
            messages.info(request,"Password minimum 8 characters")
            return redirect(admin_home_page)
        
        if not email or '@' not in email:
            messages.info(request,"Mail doesn't contain @")
            return redirect(admin_home_page)
        
        user_details = User.objects.create_user(username=user,password=password,email=email)
        user_details.save()
        return redirect(admin_home_page)

# editing the user
def admin_edit(request,id):
    if request.method == "POST" and request.user.is_superuser:
        user = User.objects.get(id=id)
        name = request.POST['username']
        email = request.POST['user_email']
        password = request.POST['password']
        con_password = request.POST['confirm_password']
        try:
            if User.objects.filter(~Q(id=id), email=email).get():
                messages.warning(request,"email is taken")
                return redirect(admin_home_page)
        except:
            pass
        try:
            if User.object.get(username = name):
                messages.warning(request,"username is taken")
                return redirect(admin_home_page)
        except:
            pass
        if len(password) < 8:
            messages.success(request,'passwaord mim length 8')
            return redirect(admin_home_page)
        if password == con_password:
            user.password = make_password(password)
        else:
            messages.success(request,'passwaord dosn\'t match')
            return redirect(admin_home_page)

        user.username = name
        user.email = email
        user.save()
        return redirect(admin_home_page)
        

# deleting an existing user
def admin_delete(request,id):
    if request.method == "POST" and request.user.is_superuser:
        instance = User.objects.get(id=id)
        instance.delete()
        user = User.objects.all().order_by('id')
        return render(request,'admin/admin_home.html',{ 'users' : user})

# search user
def admin_search(request):
    if request.method == "POST" and request.user.is_superuser:
        user_details = request.POST['search']
        if user_details: 
            user = User.objects.filter(username__icontains=user_details)
            return render(request, 'admin/admin_home.html', { 'users' : user}) 