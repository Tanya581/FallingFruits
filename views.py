from django.shortcuts import render, redirect
from .models import *
import csv, io 
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib import messages

# Create your views here.
def logout(request):
    auth.logout(request)
    return redirect('dashboard')

def login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request,'Invalid Username/Password.')
            return redirect('login')

    return render(request,'ecommerce/login.html')

def register(request):

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username Already Exists')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email Already Exists')
                return redirect('register')  
            else:      
                user = User.objects.create_user(username = username,password=password1,email=email,first_name=first_name,last_name=last_name)
                user.save()
                print('user created.')
                return redirect('login')
        else:
            messages.info(request,'Password Not Match!')
            return redirect('register')

        

    else:    
        return render(request,'ecommerce/register.html')

def sample(request):
    locations = Location.objects.all()
    context = {'locations':locations}
    return render(request,'ecommerce/sample.html',context)

def dashboard(request):
    products = Product.objects.all()
    context = {'products':products}
    if request.method == "POST":
        return redirect('cart')

    return render(request,'ecommerce/dashboard.html',context)

@login_required(login_url='login')
def cart(request):
    context ={}
    return render(request,'ecommerce/cart.html',context)


def maps(request):
    return render(request,'ecommerce/map.html')


def contactus(request):
    return render(request,'ecommerce/contact-us.html')














@permission_required('admin_can_add_log_entry')
def location_upload(request):
    prompt = {
        'order':'Order of CSV should be state, city, latitude,longitude,farm'
    }    

    if request.method == 'GET':
        return render(request,'ecommerce/location_upload.html',prompt)

    csv_file = request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'This is not a csv file')    

    data_set = csv_file.read().decode('unicode_escape')
    io_string = io.StringIO(data_set)
    next(io_string) 

    for column in csv.reader(io_string, delimiter= ',', quotechar="|"):
        _, created = Location.objects.update_or_create(
            state = column[0],
            city = column[1],
            latitude = column[2],
            longitude = column[3],
            farm = column[4]
        )  

    context = {}
    return render(request,'ecommerce/location_upload.html',context)