from django.shortcuts import render
from django.forms import inlineformset_factory
from django.views.generic import ListView, CreateView, UpdateView
from ordersapp.models import Order, OrderItem
from django.urls import reverse_lazy
from django.db import transaction
from basket.models import Basket
from ordersapp.forms import OrderItemForm


class OrderList(ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderCreate(CreateView):
    model = Order
    fields = ()
    success_url = reverse_lazy("orders:order_list")

    def get_context_data(self, **kwargs):
        context = super(OrderCreate, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            basket_item = Basket.objects.filter(user=self.request.user)
            if len(basket_item):
                OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=len(basket_item))
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial["product"] = basket_item[num].product
                    form.initial["quantity"] = basket_item[num].quantity
                    form.initial["price"] = basket_item[num].product.price
                basket_item.detele()
            else:
                formset = OrderFormSet()

        context["orderitems"] = formset
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context["orderitems"]
        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super(OrderCreate, self).form_valid(form)


class OrderUpdate(UpdateView):
    model = Order
    fields = ()
    success_url = reverse_lazy("orders:orders_list")

    def get_context_data(self, **kwargs):
        context = super(OrderCreate, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            basket_item = Basket.objects.filter(user=self.request.user)
            if len(basket_item):
                OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=len(basket_item))
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial["product"] = basket_item[num].product
                    form.initial["quantity"] = basket_item[num].quantity
                    form.initial["price"] = basket_item[num].product.price
                basket_item.detele()
            else:
                formset = OrderFormSet()

        context["orderitems"] = formset
        return context