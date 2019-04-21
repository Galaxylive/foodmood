from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required

from foodtaskerapp.forms import UserForm , RestaurentForm,UserFormForEdit,MealForm
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from foodtaskerapp.models import Meals,Order

# Create your views here.
def home(request):
    return redirect(restaurent_home)

@login_required(login_url = '/restaurent/sign-in/')
def restaurent_home(request):
    return redirect(restaurent_order)

@login_required(login_url = '/restaurent/sign-in/')
def restaurent_account(request):
    user_form = UserFormForEdit(instance = request.user)
    restaurent_form = RestaurentForm(instance = request.user.restaurent)

    if request.method == "POST":
        user_form = UserFormForEdit(request.POST, instance= request.user)
        restaurent_form = RestaurentForm(request.POST, request.FILES, instance= request.user.restaurent)

        if user_form.is_valid() and restaurent_form.is_valid():
            user_form.save()
            restaurent_form.save()

    return render(request,'restaurent/account.html',{
        "user_form": user_form,
        "restaurent_form": restaurent_form
    })

@login_required(login_url = '/restaurent/sign-in/')
def restaurent_meal(request):

    meals = Meals.objects.filter(restaurent = request.user.restaurent).order_by("-id")
    return render(request,'restaurent/meal.html',{"meals": meals})

@login_required(login_url = '/restaurent/sign-in/')
def restaurent_add_meal(request):
    form = MealForm()

    if request.method == "POST":
        form = MealForm(request.POST, request.FILES)

        if form.is_valid():
            meal = form.save(commit = False)
            meal.restaurent = request.user.restaurent
            meal.save()
            return redirect(restaurent_meal)

    return render(request,'restaurent/add_meal.html',{
        "form":form
    })

@login_required(login_url = '/restaurent/sign-in/')
def restaurent_edit_meal(request,meal_id):
    form = MealForm(instance = Meals.objects.get(id = meal_id))

    if request.method == "POST":
        form = MealForm(request.POST, request.FILES,instance = Meals.objects.get(id = meal_id))

        if form.is_valid():
            form.save()
            return redirect(restaurent_meal)

    return render(request,'restaurent/edit_meal.html',{
        "form":form
    })


@login_required(login_url = '/restaurent/sign-in/')
def restaurent_order(request):
    if request.method == "POST":
        order = Order.objects.get(id = request.POST["id"],restaurent = request.user.restaurent)

        if order.status == Order.COOKING: 
            order.status = Order.READY
            order.save()

    orders = Order.objects.filter(restaurent = request.user.restaurent).order_by("-id")
    return render(request,'restaurent/order.html',{ "orders":orders})


@login_required(login_url = '/restaurent/sign-in/')
def restaurent_report(request):
    return render(request,'restaurent/report.html',{})

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
