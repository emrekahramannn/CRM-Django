from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Record
from .forms import SignUpForm, AddRecordForm


def home(request):
    # Integrated Login View
    
    # Check to see if loggin in
    if request.method == "POST":
        post_info = request.POST
        username = post_info.get("username")
        password = post_info.get("password")

        # Check for credentials
        if len(username) <= 0 or len(password) <= 0:
            messages.warning(request, "Please fill out the form to log in")
            return redirect('home')

        # Authenticate
        user_login = authenticate(request, username = 
        username, password = password)
        if user_login is not None:
            login(request, user_login)
            messages.success(request, f"{request.user.username}, you logged in.")
            return redirect('home')
        # If not authenticated
        messages.error(request, "Wrong username or password")
        return redirect('home')

    # if user logged in show records
    records = Record.objects.all()
    context = dict(
        records = records,
    )
    return render(request, 'website/home.html', context)


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect('home')


def register_user(request):
    form = SignUpForm()
    
    if request.method == "POST":
        form = SignUpForm(request.POST or None)
        
        if form.is_valid():
            form.save()

            # Authenticated and login
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            user_login = authenticate(request, username = username, password = password)
            
            login(request, user_login)
            return redirect('home')
            messages.success(request,"You have successfully registered.")

    context = dict(
        form = form,
    )
    return render(request, 'website/register.html', context)


@login_required(login_url='home')
def customer_record(request, id):
    if request.user.is_authenticated:
        customer_record = get_object_or_404(Record, pk = id)
        context = dict(
            customer_record = customer_record,
        )
        return render(request, 'website/record.html', context)
    
    messages.info(request, "You must be logged in to view that page.")
    return redirect('home')


@login_required(login_url='home')
def delete_record(request, id):
    if request.user.is_authenticated:
        customer_record = get_object_or_404(Record, pk = id)
        customer_record.delete()
        messages.success(request, "Record deleted successfully.")
        return redirect('home')
    return redirect('home') 


@login_required(login_url='home')
def add_record(request):
    form = AddRecordForm(request.POST or None)

    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record added successfully.")
                return redirect('home')
        return render(request, 'website/add_record.html', {'form': form})
    else:
        messages.info(request, "You must be logged in to add record.")
        return redirect('home')
    

@login_required(login_url='home')
def update_record(request, id):
    form = AddRecordForm()
    if request.user.is_authenticated:
        record = get_object_or_404(Record, pk = id)
        form = AddRecordForm(request.POST or None, 
        instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record has been updated.")
            return redirect('home')
        
        return render(request, 'website/update_record.html', {'form': form})
    
    messages.info(request, 'You must be logged in to access this page.')
    return redirect('home')
