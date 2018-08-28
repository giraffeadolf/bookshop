from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from mainapp.views import basket_view
from django.contrib.auth.decorators import login_required
from basketapp.models import Basket
from mainapp.models import Book
from django.urls import reverse
from django.template.loader import render_to_string
from django.http import JsonResponse, Http404


@login_required
def basket_add(request, pk):
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('catalog:book', args=[pk]))

    book = get_object_or_404(Book, pk=pk)
    old_basket_item = Basket.objects.filter(user=request.user, book=book)

    if old_basket_item:
        old_basket_item[0].quantity += 1
        old_basket_item[0].save()
    else:
        new_basket_item = Basket(user=request.user, book=book)
        new_basket_item.quantity += 1
        new_basket_item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove(request, pk):
    if request.method == 'GET':
        basket_record = get_object_or_404(Basket, pk=pk)
        basket_record.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        raise Http404


@login_required
def basket_remove_all(request):
    if request.method == 'GET':
        basket = Basket.objects.filter(user=request.user)
        for item in basket:
            item.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        raise Http404


@login_required
def basket_edit(request, pk, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        new_basket_item = Basket.objects.get(pk=int(pk))

        if quantity > 0:
            new_basket_item.quantity = quantity
            new_basket_item.save()
        else:
            new_basket_item.delete()

        basket_items = Basket.objects.filter(user=request.user).order_by('book__category')

        content = {
            'basket_items': basket_items,
        }

        result = render_to_string('basketapp/includes/inc_basket_list.html', content)

        return JsonResponse({'result': result})
