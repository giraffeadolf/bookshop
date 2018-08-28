from django.shortcuts import render, HttpResponseRedirect, HttpResponse, get_object_or_404
from .models import Book, BookCategory
from basketapp.models import Basket
from authapp.forms import ShopUserContactForm
from django.urls import reverse
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random
from logger.logger_config import log


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    else:
        return []


def get_bestseller():
    books = Book.objects.filter(is_active=True, category__is_active=True)

    return random.sample(list(books), 1)[0]


def get_same_books(bestseller):
    same_books = Book.objects.filter(category=bestseller.category, is_active=True, category__is_active=True).exclude(pk=bestseller.pk)[:4]

    return same_books


@log('Main page is active')
def main(request):
    bestseller = get_bestseller()
    same_books = get_same_books(bestseller)
    new_books = Book.objects.filter(is_active=True, category__is_active=True)[14:20]
    basket = get_basket(user=request.user)
    content = {'basket': basket, 'new_books': new_books, 'bestseller': bestseller, 'same_books': same_books}
    return render(request, 'mainapp/index.html', content)


@log('Basket is active')
@login_required
def basket_view(request):
    basket = get_basket(user=request.user)
    basket_items = basket.order_by('book__category')
    content = {'basket': basket, 'basket_items': basket_items}
    return render(request, 'mainapp/basket.html', content)


@log('Catalog is active')
def catalog(request, pk=None, page=1):
    print(pk)
    links_menu = BookCategory.objects.filter(is_active=True)
    book_list = Book.objects.filter(is_active=True, category__is_active=True)
    new_books = Book.objects.filter(is_active=True, category__is_active=True)[14:20]

    paginator = Paginator(book_list, 10)
    try:
        books_paginator = paginator.page(page)
    except PageNotAnInteger:
        books_paginator = paginator.page(1)
    except EmptyPage:
        books_paginator = paginator.page(paginator.num_pages)

    basket = get_basket(user=request.user)

    if pk:
        if pk == '0':
            category = {'name': 'Все жанры'}
            book_list = Book.objects.filter(is_active=True, category__is_active=True)
        else:
            category = get_object_or_404(BookCategory, pk=pk, is_active=True)
            category_len = Book.objects.filter(category=category)
            book_list = Book.objects.filter(category__pk=pk, is_active=True, category__is_active=True)
        paginator = Paginator(book_list, 10)
        try:
            books_paginator = paginator.page(page)
        except PageNotAnInteger:
            books_paginator = paginator.page(1)
        except EmptyPage:
            books_paginator = paginator.page(paginator.num_pages)
        content = {
            'links_menu': links_menu,
            'book_list': books_paginator,
            'category': category,
            'category_len': category_len,
            'basket': basket,
            'new_books': new_books,
        }
        return render(request, 'mainapp/catalog.html', content)

    content = {
        'links_menu': links_menu,
        'book_list': books_paginator,
        'basket': basket,
        'new_books': new_books,
    }
    return render(request, 'mainapp/catalog.html', content)


@log('Book page is active')
def book_page(request, pk):
    book = get_object_or_404(Book, pk=pk, is_active=True, category__is_active=True)
    same_books = Book.objects.filter(category__pk=book.category.pk, is_active=True, category__is_active=True).exclude(pk=book.pk)[:6]

    basket = get_basket(user=request.user)

    content = {
        'links_menu': BookCategory.objects.all(),
        'book': book,
        'same_books': same_books,
        'basket': basket
    }

    return render(request, 'mainapp/book.html', content)


@log('Contact page is active')
def contact(request):
    basket = get_basket(user=request.user)

    if request.method == 'POST':
        contact_form = ShopUserContactForm(request.POST)
        username = request.POST['username']
        email = request.POST['email']
        theme = request.POST['theme']
        data = request.POST['data']
        if username and email and theme and data:
            try:
                send_mail('{} : {}'.format(username, theme), data, email, ['toscha.nv@gmail.com'], fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return HttpResponseRedirect(reverse('contact'))
    else:
        contact_form = ShopUserContactForm()
    content = {'contact_form': contact_form, 'basket': basket}
    return render(request, 'mainapp/contact.html', content)


@log('Shares page is active')
def shares(request):
    bestseller1 = get_bestseller()
    bestseller2 = get_bestseller()
    same_books1 = get_same_books(bestseller1)
    same_books2 = get_same_books(bestseller2)
    basket = get_basket(user=request.user)
    content = {
        'basket': basket,
        'bestseller1': bestseller1,
        'bestseller2': bestseller2,
        'same_books1': same_books1,
        'same_books2': same_books2
    }
    return render(request, 'mainapp/shares.html', content)
