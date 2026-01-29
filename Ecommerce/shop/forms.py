from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email','username', 'password1', 'password2']


from django import forms
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


from shop.models import Category
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"


from shop.models import Product
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','description','image','price','stock','category']


class StockForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['stock',]