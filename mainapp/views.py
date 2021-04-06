from django.shortcuts import render
from json import load
from mainapp.models import Product, ProductCategory

# MVT = model view template
# контроллеры
# в mainapp создаем каталог -> templates
# папка templates подключена

def index(request):
    context = {"title" : "GeekShop"}
    return render(request, "mainapp/index.html", context)  # первый параметр сам req, и путь до шаблона index.html

def products(request, id=None):
    data = {
        "title": "GeekShop - Каталог",
        "products":  Product.objects.all(),
        "categories": ProductCategory.objects.all(),
    }
   # print(id)
    return render(request, "mainapp/products.html", data)

def products_by_category(request, category_id=None):
    data = {
        "title": "GeekShop - Каталог",
        "products": Product.objects.filter(category_id=category_id),
        "categories": ProductCategory.objects.all()
    }
    return render(request, "mainapp/products.html", data)
