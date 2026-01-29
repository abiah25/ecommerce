from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views import View
from shop.models import Category

class CategoryView(View):
    def get(self,request):
        c=Category.objects.all()
        context={'categories':c}
        return render(request,'categories.html', context)


class CategoryProducts(View):
    def get(self,request,i):
        c=Category.objects.get(id=i)
        context={'category':c}
        return render(request,"products.html",context)

from shop.forms import SignupForm
class Register(View):
    def get(self,request):
        form_instance=SignupForm()
        context={'form':form_instance}
        return render(request,"register.html",context)
    def post(self,request):
        form_instance = SignupForm(request.POST,request.FILES)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:categories')


from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from shop.forms import LoginForm
class Login(View):
    def get(self,request):
        form_instance=LoginForm()
        context={'form':form_instance}
        return render(request,"login.html",context)
    def post(self,request):
        form_instance=LoginForm(request.POST)
        if form_instance.is_valid():
            data=form_instance.cleaned_data
            print(data)
            u=data['username']
            p=data['password']
            user=authenticate(username=u,password=p)

            if user and user.is_superuser==True:
                login(request,user)
                return redirect('shop:categories')
            elif user and user.is_superuser==False:
                login(request, user)
                return redirect('shop:categories')
            else:
                messages.error(request,'Invalid user credentials')
                return redirect('shop:login')


class Logout(View):
    def get(self,request):
        logout(request)
        return redirect("shop:login")

from shop.models import Product
class ProductDetails(View):
    def get(self,request,i):
        p=Product.objects.get(id=i)
        context={'product':p}
        return render(request,"productdetail.html",context)

def admin_required(fun):
    def wrapper(request):
        if not request.user.is_superuser:
            return HttpResponse('Admin User Only')
        else:
            return fun(request)
    return wrapper


from shop.forms import CategoryForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
@method_decorator(login_required,name="dispatch")
@method_decorator(admin_required,name="dispatch")
class AddCategory(View):
    def get(self,request):
        form_instance=CategoryForm()
        context={'form':form_instance}
        return render(request,"addcategory.html",context)
    def post(self,request):
        form_instance = CategoryForm(request.POST,request.FILES)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:categories')


from shop.forms import ProductForm,StockForm
@method_decorator(login_required,name="dispatch")
@method_decorator(admin_required,name="dispatch")
class AddProduct(View):
    def get(self,request):
        form_instance=ProductForm()
        context={'form':form_instance}
        return render(request,"addproduct.html",context)
    def post(self,request):
        form_instance = ProductForm(request.POST,request.FILES)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:categories')


@method_decorator(login_required,name="dispatch")
@method_decorator(admin_required,name="dispatch")
class AddStock(View):
    def get(self,request,i):
        d = Product.objects.get(id=i)
        form_instance = StockForm(instance=d)
        context = {'form':form_instance}
        return render(request,"addstock.html", context)
    def post(self,request,i):
        d = Product.objects.get(id=i)
        form_instance = StockForm(request.POST, request.FILES,instance=d)
        if form_instance.is_valid():
            form_instance.save()
            return redirect("shop:categories")