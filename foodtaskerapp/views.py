from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from foodtaskerapp.forms import UserForm , RestaurentForm
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User

# Create your views here.
def home(request):
    return redirect(restaurent_home)

@login_required(login_url = '/restaurent/sign-in/')
def restaurent_home(request):
    return render(request,'restaurent/home.html',{})

def restaurent_sign_up(request):

    user_form = UserForm()
    restaurent_form = RestaurentForm()

    if request.method == "POST":
        user_form = UserForm(request.POST)
        restaurent_form = RestaurentForm(request.POST, request.FILES)

        if user_form.is_valid() and restaurent_form.is_valid():
            new_user = User.objects.create_user(** user_form.cleaned_data)
            new_restaurent = restaurent_form.save(commit=False)
            new_restaurent.user = new_user
            new_restaurent.save()

            login(request,authenticate(
                username = user_form.cleaned_data['username'],
                password = user_form.cleaned_data['password']
            ))
            return redirect(restaurent_home)

    return render(request,'restaurent/sign_up.html',{
        "user_form" : user_form,
        "restaurent_form" : restaurent_form
    })
