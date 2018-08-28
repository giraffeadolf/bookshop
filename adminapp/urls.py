from django.urls import path
import adminapp.views as adminapp

app_name = 'adminapp'

urlpatterns = [
    path('users/read/', adminapp.UserListView.as_view(), name='users'),
    path('users/create/', adminapp.UserCreateView.as_view(), name='user_create'),
    path('users/update/<int:pk>/', adminapp.UserUpdateView.as_view(), name='user_update'),
    path('users/delete/<int:pk>/', adminapp.UserDeleteView.as_view(), name='user_delete'),

    path('categories/read/', adminapp.categories, name='categories'),
    path('categories/create/', adminapp.category_create, name='category_create'),
    path('categories/update/<int:pk>/', adminapp.category_update, name='category_update'),
    path('categories/delete/<int:pk>/', adminapp.category_delete, name='category_delete'),

    path('books/read/category/<int:pk>/', adminapp.books, name='books'),
    path('books/create/category/<int:pk>/', adminapp.book_create, name='book_create'),
    path('books/read/<int:pk>/', adminapp.BookDetailView.as_view(), name='book_read'),
    path('books/update/<int:pk>/', adminapp.book_update, name='book_update'),
    path('books/delete/<int:pk>/', adminapp.book_delete, name='book_delete'),
]
