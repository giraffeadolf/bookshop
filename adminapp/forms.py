from django import forms
from authapp.models import ShopUser
from authapp.forms import ShopUserEditForm
from mainapp.models import BookCategory, Book


class ShopUserAdminEditForm(ShopUserEditForm):
    class Meta:
        model = ShopUser
        fields = '__all__'


class BookCategoryEditForm(forms.ModelForm):
    class Meta:
        model = BookCategory
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(BookCategoryEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class BookEditForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(BookEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
