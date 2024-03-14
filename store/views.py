from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django import forms
from django.db.models import Q
from django.core.paginator import Paginator


def home(request):
    products = Product.objects.all()

    paginator = Paginator(products, 5)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    return render(request, "index.html", {"products": products})



def about(request):
    return render(request, "about.html", {})



def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, ("You have been logged in !"))
            return redirect("home")
        else:
            messages.success(request, ("There was an error, please try again."))
            return redirect("login")
        
    else: 
        return render(request, "login.html", {})
    


def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out."))
    return redirect("home")



def register_user(request):
    form = SignUpForm()

    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, ("You have registered succesfully! Please fill out your user info below..."))
            return redirect("update_info")
        
        else:
            messages.success(request, ("Whoops! We have a problem with that registration."))
            return render(request, "register.html", {"form": form})
    else:  
        return render(request, "register.html", {"form": form})
    


def product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, "product.html", {"product": product})



def category(request, foo):
    foo = foo.replace("-", " ")

    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        product_count = products.count()  
        return render(request, "category.html", {"products": products, "category": category, "product_count": product_count})
    
    except Category.DoesNotExist:
        messages.error(request, "That category doesn't exist.")
        return redirect("home")



def update_user(request):
    if request.user.is_authenticated:
        # Get current user ID
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, "User Has Been Updated!")
            return redirect("home")
        return render(request, "update_user.html", {"user_form": user_form})
    
    else:
        messages.success(request, "You must me logged in to access that page!")
        return redirect("home")
    


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user

        if request.method == "POST":
            form = ChangePasswordForm(current_user, request.POST)

            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been updated! ")
                login(request, current_user)
                return redirect("home")

            else:
                for error in list (form.errors.values()):
                    messages.error(request, error)
                    return render(request, "update_password.html", {"form": form})

        else:
            form = ChangePasswordForm(current_user)
            return render(request, "update_password.html", {"form": form})
    else:
        messages.error(request, "You must me logged in to access that page!")


def update_info(request):
    if request.user.is_authenticated:
        # Get current user ID
        current_user = Profile.objects.get(user__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)

        if form.is_valid():
            form.save()
            messages.success(request, "Your info has been updated!")
            return redirect("home")
        
        return render(request, "update_info.html", {"form": form})
    
    else:
        messages.success(request, "You must me logged in to access that page!")
        return redirect("home")
    

def search(request):
    if request.method == "GET":
        searched = request.GET.get("searched")
        products = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        product_count = products.count() 

        if products != '' and products is not None:
            messages.success(request, "That Product Does Not Exist...Please try Again.")
            return render(request, "search.html", {'products': []})  
        else:
            return render(request, "search.html", {'products': products, 'searched': searched, 'product_count': product_count})  
    else:
        return redirect('home')  