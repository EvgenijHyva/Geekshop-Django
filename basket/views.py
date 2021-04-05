from django.shortcuts import HttpResponseRedirect, get_object_or_404
from mainapp.models import Product
from basket.models import Basket
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse

# для вывода не нужно подготавливать шаблон так как шаблон подготовлен
# для использования подключеных шаблонов используется {% includes %}

@login_required
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

@login_required
def basket_remove(request, id):
    basket = Basket.objects.get(id=id)
    basket.delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

def basket_edit(request, id, quantity):  # контроллер отвечающий за редактирование корзины
    # template: http://localhost:8000/baskets/edit/31/3/
    if request.is_ajax():
        quantity = int(quantity)  # str
        basket = Basket.objects.get(id=int(id))  # str
        if quantity > 0:
            basket.quantity = quantity
            basket.save()
        else:
            basket.delete()
        baskets = Basket.objects.filter(user=request.user)
        context = {
            "baskets": baskets
        }
        result = render_to_string("basket/basket.html", context)
        return JsonResponse({"result": result})
