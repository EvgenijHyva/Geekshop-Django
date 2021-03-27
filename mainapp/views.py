from django.shortcuts import render
from json import load
from mainapp.models import Product,ProductCategory

# MVT = model view template
# контроллеры
# в mainapp создаем каталог -> templates
# папка templates подключена

def index(request):
    context = {"title" : "GeekShop"}
    return render(request, "mainapp/index.html", context)  # первый параметр сам req, и путь до шаблона index.html

def products(request):
    with open("mainapp/fixtures/products.json", "r", encoding="utf-8") as file:
        context = load(file)
        for i in context["products"]:
            i["inCart"] = eval(i["inCart"])
    data = {
        "products": Product.objects.all(),
        "categories": ProductCategory.objects.all(),
    }
    return render(request, "mainapp/products.html", data)
