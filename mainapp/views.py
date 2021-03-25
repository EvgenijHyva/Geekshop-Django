from django.shortcuts import render


# MVT = model view template
# контроллеры
# в mainapp создаем каталог -> templates
# папка templates подключена

def index(request):
    return render(request, "mainapp/index.html")  # первый параметр сам req, и путь до шаблона index.html

def products(request):
    return render(request, "mainapp/products.html")