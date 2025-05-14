from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm

from payment.forms import ShippingForm
from payment.models import ShippingAddress

from django import forms
from django.db.models import Q
import json
from cart.cart import Cart

def search(request):
    # Determine if they filled out the form
    if request.method == "POST":
        searched = request.POST['searched']
        #Query the Prodects DB Model
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        #Test for null
        if not searched:
            messages.success(request, "No products matched your search. Please try again with a different keyword.")
            return render(request, "search.html", {})
        else:
            return render(request, "search.html", {'searched':searched})
    else:
        return render(request, "search.html", {})

def updateInfo(request):
    if request.user.is_authenticated:
        #Get Current User
        currentUser = Profile.objects.get(user__id=request.user.id)
        #Get Current User's Shipping Info
        shippingUser = ShippingAddress.objects.get(user__id=request.user.id)
        #Get original User Form
        form = UserInfoForm(request.POST or None, instance=currentUser)
        #Get User's Shipping Form
        shipping_form = ShippingForm(request.POST or None, instance=shippingUser)
        if form.is_valid() or shipping_form.is_valid():
            #Save original form
            form.save()
            #Save Shipping Form
            shipping_form.save()
            messages.success(request, "Your profile information has been successfully updated.")
            return redirect('home')
       
        return render(request, "updateInfo.html", {'form': form, 'shipping_form': shipping_form})
    else:
        messages.warning(request, "You need to be logged in to access this page.")
        return redirect('home')

def updatePassword(request):
    if request.user.is_authenticated:
        currentUser = request.user
        # Did they fill out the form
        if request.method == 'POST':
            form = ChangePasswordForm(currentUser, request.POST)
            # Is the form valid
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been successfully updated.")
                login(request, currentUser)
                return redirect('updateUser')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('updatePassword')
        else:
            form = ChangePasswordForm(currentUser)
            return render(request, "updatePassword.html", {'form':form})
    else:
        messages.warning(request, "You must be logged in to access that page.")
        return redirect('home')

def updateUser(request):
    if request.user.is_authenticated:
        currentUser = User.objects.get(id=request.user.id)
        userForm = UpdateUserForm(request.POST or None, instance=currentUser)
        if userForm.is_valid():
            userForm.save()
        
            login(request, currentUser)
            messages.success(request, "Your account details have been updated.")
            return redirect('home')
       
        return render(request, 'updateUser.html', {"userForm": userForm})
    else:
        messages.warning(request, "You must be logged in to access that page.")
        return redirect('home')

def categorySummary(request):
    categories = Category.objects.all()
    return render(request, 'categorySummary.html', {"categories":categories} )
def category(request, foo):
    #Replace Hyphens with Spaces
    foo = foo.replace('-', '')
    #Grab the category from the url
    try:
        #Look up the Category
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products':products, 'category':category})
    except:
        messages.error(request, "The requested category does not exist.")
        return redirect('home')

def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product':product})

def home(request):
    products = Product.objects.all()[:24]
    return render(request, 'home.html', {'products': products})

def about(request):
    return render(request, 'about.html', {})

def loginUser(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            #Do dome shopping cart stuff
            currentUser = Profile.objects.get(user__id=request.user.id)
            #Get their saved cart from database
            saved_cart = currentUser.old_cart
            #Convert database string to python dictionary
            if saved_cart:
                #Convert to dictionary using JSON
                converted_cart = json.loads(saved_cart)
                #Add the loaded cart dictionary to our session
                #Get the cart
                cart = Cart(request)
                #Loop through the cart and add the items from the database
                for key,value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)
            messages.success(request, ("You have successfully logged in."))
            return redirect('home')
        else:
            messages.error(request, "Invalid login credentials. Please try again.")
            return redirect('login')
        
    else:
        return render(request, 'login.html', {})

def logoutUser(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')

def registerUser(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            #Log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Account created successfully. Please complete your profile.")
            return redirect('updateInfo')
        else:
            messages.error(request, "There was an error during registration. Please correct the form and try again.")
            return redirect('register')
    else:
        return render(request, 'register.html', {'form':form})

