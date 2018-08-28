from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from authapp.models import ShopUser
from mainapp.models import BookCategory, Book
from authapp.forms import ShopUserRegistrationForm
from adminapp.forms import ShopUserAdminEditForm, BookCategoryEditForm, BookEditForm
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator


class UserListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(UserListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['title'] = 'Пользователи'
        return context


class UserCreateView(CreateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin:users')
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Создание пользователя'
        return context


class UserUpdateView(UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin:users')
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Редактирование'
        return context


class UserDeleteView(DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    success_url = reverse_lazy('admin:users')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(UserDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'Удаление'
        return context


@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    title = 'Категории'
    categories_list = BookCategory.objects.all()

    content = {
        'title': title,
        'objects': categories_list,
    }

    return render(request, 'adminapp/categories.html', content)


@user_passes_test(lambda u: u.is_superuser)
def category_create(request):
    title = 'Создание категории'

    if request.method == 'POST':
        category_form = BookCategoryEditForm(request.POST, request.FILES)
        if category_form.is_valid():
            category_form.save()
    else:
        category_form = BookCategoryEditForm()

    content = {
        'title': title,
        'form': category_form,
    }

    return render(request, 'adminapp/category_update.html', content)


@user_passes_test(lambda u: u.is_superuser)
def category_update(request, pk):
    title = 'Редактирование'
    edit_category = get_object_or_404(BookCategory, pk=pk)

    if request.method == 'POST':
        edit_form = BookCategoryEditForm(request.POST, request.FILES, instance=edit_category)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:category_update', args=[edit_category.pk]))
    else:
        edit_form = BookCategoryEditForm(instance=edit_category)

    content = {
        'title': title,
        'form': edit_form,
    }

    return render(request, 'adminapp/category_update.html', content)


@user_passes_test(lambda u: u.is_superuser)
def category_delete(request, pk):
    title = 'Удаление'
    category = get_object_or_404(BookCategory, pk=pk)

    if request.method == 'POST':
        category.is_active = False
        category.save()
        return HttpResponseRedirect(reverse('admin:categories'))

    content = {
        'title': title,
        'category_to_delete': category,
    }

    return render(request, 'adminapp/category_delete.html', content)


@user_passes_test(lambda u: u.is_superuser)
def books(request, pk):
    title = 'Книги'
    category = get_object_or_404(BookCategory, pk=pk)
    books_list = Book.objects.filter(category=category)

    content = {
        'title': title,
        'category': category,
        'objects': books_list,
    }

    return render(request, 'adminapp/books.html', content)


class BookDetailView(DetailView):
    model = Book
    template_name = 'adminapp/book_read.html'

    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)
        context['title'] = 'Просмотр'
        return context


@user_passes_test(lambda u: u.is_superuser)
def book_create(request, pk):
    title = 'Создание книги'
    category = get_object_or_404(BookCategory, pk=pk)

    if request.method == 'POST':
        book_form = BookEditForm(request.POST, request.FILES)
        if book_form.is_valid():
            book_form.save()
    else:
        book_form = BookEditForm(initial={'category': category})

    content = {
        'title': title,
        'form': book_form,
        'category': category,
    }

    return render(request, 'adminapp/book_update.html', content)


@user_passes_test(lambda u: u.is_superuser)
def book_update(request, pk):
    title = 'Редактирование'
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        edit_form = BookEditForm(request.POST, request.FILES, instance=book)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:book_update', args=[book.category.pk]))
    else:
        edit_form = BookEditForm(instance=book)

    content = {
        'title': title,
        'form': edit_form,
        'category': book.category,
    }

    return render(request, 'adminapp/book_update.html', content)


@user_passes_test(lambda u: u.is_superuser)
def book_delete(request, pk):
    title = 'Удаление'
    book = get_object_or_404(Book, pk=pk)
    category = book.category

    if request.method == 'POST':
        book.is_active = False
        book.save()
        return HttpResponseRedirect(reverse('admin:books', args=[category.pk]))

    content = {
        'title': title,
        'book_to_delete': book,
        'category': category,
    }

    return render(request, 'adminapp/book_delete.html', content)
