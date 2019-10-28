import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.shortcuts import render, redirect
from products.models import Products, Preferences


def index(request):
    return render(request, 'index.html')


def search(request):
    query = request.GET.get('query')
    params = {
        "search_terms": query,
        "search_simple": 1,
        "action": "process",
        "json": 1
    }
    response = requests.get(settings.API_URL, params=params)
    data = response.json()

    if len(data["products"]) > 0:
        for product in data["products"]:
            if "product_name" in product:
                product_name = product["product_name"]
            if "image_front_url" in product:
                image = product["image_front_url"]
            if "nutrition_grades" in product:
                score = product["nutrition_grades"]
            if "ingredients_text" in product:
                ingredients = product["ingredients_text"]
            if "image_nutrition_url" in product:
                nutrition_url = product["image_nutrition_url"]
            if "url" in product:
                product_url = product["url"]
            if "categories_hierarchy" in product:
                categories = product["categories_hierarchy"][0]
            try:
                Products.objects.get(product_name=product_name)
            except Products.DoesNotExist:
                Products.objects.create(product_name=product_name,
                                        image=image,
                                        nutrition_grade=score,
                                        ingredients=ingredients,
                                        nutri_image=nutrition_url,
                                        product_url=product_url,
                                        categories=categories
                                        )
        category = data["products"][0]["categories_hierarchy"][0]
        result = Products.objects.filter(
            categories=category).order_by("nutrition_grade")[0:10]

        product_name = data["products"][0]["product_name"]
        query = Products.objects.get(product_name=product_name)
        context = {
            'result': result,
            'query': query
        }
        return render(request, "result.html", context)

    else:
        context = {
                   "no_product": True
        }
        return render(request, "result.html", context)


@login_required()
def save(request, product_id):
    product = Products.objects.get(id=product_id)
    try:
        Preferences.objects.get(product_name=product.product_name)
    except Preferences.DoesNotExist:
        Preferences.objects.create(product_name=product.product_name,
                                   image=product.image,
                                   nutrition_grade=product.nutrition_grade,
                                   nutrition_image=product.nutri_image,
                                   product_url=product.product_url)
    else:
        pass
    preference = Preferences.objects.get(product_name=product.product_name)
    user = User.objects.get(username=request.user.username)
    preference.user.add(user)
    context = {
        "name": product.product_name,
        "image": product.image,
        "nutrition_grade": product.nutrition_grade,
        "nutrition_image": product.nutri_image,
        "url": product.product_url
    }
    return render(request, "save.html", context)


@login_required()
def preferences(request):
    result = Preferences.objects.all()
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

@login_required()
def remove_preferences(request, preference_id):
    preference = Preferences.objects.get(id=preference_id)
    preference.delete()
    return render(request, "preferences.html")


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


def contact(request):
    return render(request, "contact.html")


def legal_notice(request):
    return render(request, "notice.html")
