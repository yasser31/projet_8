import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.shortcuts import render, redirect
from products.models import Products, Preferences

# index page view


def index(request):
    return render(request, 'index.html')

# the function that will handle the search


def search(request):
    if request.GET.get("query") == "":
        context = {
            "no_search": True
        }
        return render(request, "result.html", context)
    try:
        query = request.GET.get('query')
        searched_product = Products.objects.filter(
            product_name__icontains=query)[0]
        result = Products.objects.filter(
            product_name__icontains=query).order_by("nutrition_grade")[0:10]
        context = {
            'result': result,
            'query': searched_product
        }
        return render(request, "result.html", context)
    except IndexError:
        context = {
            "no_product": True
        }
        return render(request, "result.html", context)

# function that will handle saving products, used with a decorator
@login_required()
def save(request, product_id):
    product = Products.objects.get(id=product_id)
    try:
        Preferences.objects.get(product__product_name=product.product_name)
    except Preferences.DoesNotExist:
        Preferences.objects.create(product=product)
    else:
        pass
    preference = Preferences.objects.get(
        product__product_name=product.product_name)
    user = User.objects.get(username=request.user.username)
    preference.users.add(user)
    context = {
        "name": product.product_name,
        "image": product.image,
        "nutrition_grade": product.nutrition_grade,
        "nutrition_image": product.nutri_image,
        "url": product.product_url
    }
    return render(request, "save.html", context)

# details page


def details(request, product_id):
    product = Preferences.objects.get(
        id=product_id)
    context = {
        "name": product.product.product_name,
        "image": product.product.image,
        "nutrition_grade": product.product.nutrition_grade,
        "nutrition_image": product.product.nutri_image,
        "url": product.product.product_url
    }
    return render(request, "save.html", context)

# handle the acces to preferences
@login_required()
def preferences(request):
    result = Preferences.objects.filter(users__username=request.user.username)
    try:
        query = result[0]
    except IndexError:
        return render(request, "preferences.html")
    else:
        query = result[0]
        context = {
            'result': result,
            'query': query
        }
        return render(request, "preferences.html", context)

# handle preferences deletion
@login_required()
def remove_preferences(request, preference_id):
    preference_to_delete = Preferences.objects.get(id=preference_id)

    preference_to_delete.delete()
    result = Preferences.objects.filter(
        users__username=request.user.username)
    context = {
        'result': result
    }
    return render(request, "preferences.html", context)

# handle the signup


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("index")
    else:
        form = UserCreationForm()

    return render(request, "signup.html", {"form": form})

# handle the access to the contact page


def contact(request):
    return render(request, "contact.html")

# handle the access to legal notice page


def legal_notice(request):
    return render(request, "notice.html")


def account(request):
    return render(request, "account.html")
