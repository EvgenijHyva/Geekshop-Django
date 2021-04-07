from django.shortcuts import render
from json import load
from mainapp.models import Product, ProductCategory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# MVT = model view template
# контроллеры
# в mainapp создаем каталог -> templates
# папка templates подключена

def index(request):
    context = {"title": "GeekShop"}
    return render(request, "mainapp/index.html", context)  # первый параметр сам req, и путь до шаблона index.html

def products(request, product_name=None, category_id=None, page=1):
    """Paginator класс который реализует постраничный вывод"""
    data = {
        "categories": ProductCategory.objects.all(),
        "title": "GeekShop - Каталог товаров"
    }
    if product_name:  # при нажатии на отдельный товар рендерится страница с этим товаром
        data.update({
            "title": "Товар: " + str(product_name),
            "products": Product.objects.filter(name=product_name)
        })
        return render(request, "mainapp/product.html", data)

    products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()

    paginator = Paginator(object_list=products, per_page=3)
    try:  # Paginator рекомендует использовать такую конструкцию для отлова ошибок, в случае:
        products_paginator = paginator.page(number=page)  # если передастся например мистическим образом float
    except PageNotAnInteger:  # тогда перенаправит на первую страницу
        products_paginator = paginator.page(number=1)
    except EmptyPage:  # если пустая страница, тогда отображаем все товары
        products_paginator = paginator.page(paginator.num_pages)

    data.update({
        "products": products_paginator
    })
    return render(request, "mainapp/products.html", data)
