from django.shortcuts import HttpResponseRedirect, get_object_or_404
from mainapp.models import Product
from basket.models import Basket

# для вывода не нужно подготавливать шаблон так как шаблон подготовлен
# для использования подключеных шаблонов используется {% includes %}

def basket_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    #print(product)
    baskets = Basket.objects.filter(user=request.user, product=product)
    if not baskets.exists():
        basket = Basket(user=request.user, product=product)
        basket.quantity += 1
        basket.save()
    else:
        basket = baskets.first()
        print(f"baskets: {baskets}")
        basket.quantity += 1
        basket.save()
    # print(f"Meta: {request.META['HTTP_REFERER']}")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

def basket_remove(request, id):
    basket = Basket.objects.get(id=id)
    basket.delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))