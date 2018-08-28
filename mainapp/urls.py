from django.urls import path
import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.catalog, name='index'),
    path('category/<int:pk>/', mainapp.catalog, name='category'),
    path('book/<int:pk>/', mainapp.book_page, name='book'),
    path('category/<int:pk>/page/<int:page>/', mainapp.catalog, name='page')
]
