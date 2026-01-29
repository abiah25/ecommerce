from django.shortcuts import render, redirect
from django.views import View
from shop.models import Product
from cart.models import Cart
import uuid
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

import razorpay

# Create your views here.

@method_decorator(login_required,name="dispatch")
class AddtoCart(View):  #To add items to Cart Table
    def get(self, request,i):
        p=Product.objects.get(id=i)
        u=request.user  #logged user
        try:
            c=Cart.objects.get(user=u,product=p)   #check whether that product
                                                   #is already placed into cart table by the user
                                                   #if yes increments its quantity by 1
            c.quantity+=1
            c.save()
        except:  #else if product does not exist
            c=Cart.objects.create(user=u,product=p,quantity=1)  #creates new record with quantity 1
            c.save()
        return redirect('cart:cartview')

@method_decorator(login_required,name="dispatch")
class CartView(View):   #To display cart items selected by the current user
    def get(self,request):
        u=request.user
        c=Cart.objects.filter(user=u)
        total=0
        for i in c:
            total+=i.subtotal()
        context={'cart':c,'total':total}
        return render(request,'cart.html',context)


@method_decorator(login_required,name="dispatch")
class CartDecrement(View):
    def get(self,request,i):
        try:
            c=Cart.objects.get(id=i)
            if c.quantity>1:
                c.quantity-=1
                c.save()
            else:
                c.delete()
        except:
            pass

        return redirect('cart:cartview')

@method_decorator(login_required,name="dispatch")
class CartRemove(View):
    def get(self,request,i):
        try:
            c=Cart.objects.get(id=i)
            c.delete()
        except:
            pass

        return redirect('cart:cartview')

from cart.models import OrderItems
from cart.forms import OrderForm
@method_decorator(login_required,name="dispatch")
class Checkout(View):
    def post(self,request):
        print(request.POST)
        form_instance = OrderForm(request.POST)
        if form_instance.is_valid():
            o=form_instance.save(commit=False)

            #user
            u=request.user
            o.user=u

            #order amount
            c=Cart.objects.filter(user=u)
            total=0
            for i in c:
                total+=i.subtotal()
            print(total)
            o.amount=int(total)
            o.save()
            if(o.payment_method=="ONLINE"):
                #1. Razorpay client connection
                client=razorpay.Client(auth=('rzp_test_S60HbKfEAaQCrF','3k1kU8qXliCw9ZRJaMREofsu'))
                print(client)


                #2. Place order
                response_payment=client.order.create(dict(amount=o.amount*100,currency='INR'))
                print(response_payment)
                id=response_payment['id']
                o.order_id=id
                o.save()
                context={'payment':response_payment}
            else:
                id=uuid.uuid4().hex[:14]   #manually creates orderid for order
                o.order_id='order_COD'+id
                o.is_ordered=True
                o.save()
                for i in c:
                    items=OrderItems.objects.create(order=o,product=i.product,quantity=i.quantity)
                    items.save()
                    items.product.stock -= items.quantity
                    items.product.save()
                c.delete()
                return render(request, 'payment.html')
            return render(request,'payment.html',context)


    def get(self,request):
        form_instance=OrderForm()
        context={'form':form_instance}
        return render(request,'checkout.html',context)


from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from cart.models import Order
from django.contrib.auth.models import User
from django.contrib.auth import login
@method_decorator(login_required,name="dispatch")
@method_decorator(csrf_exempt,name="dispatch")
class PaymentSuccess(View):
    def post(self,request,i):
        print(request.POST)

        u=User.objects.get(username=i)
        login(request,u)

        id=request.POST['razorpay_order_id']

        #order
        o=Order.objects.get(order_id=id)
        o.is_ordered=True  #Mark Order as Completed
        o.save()

        #Move Cart Items → Order Items
        #orderitems
        #cart
        c=Cart.objects.filter(user=request.user)   #Gets all cart products of logged-in user.
        for i in c:   #Each i is a cart object:
            item = OrderItems.objects.create(order=o,product=i.product,quantity=i.quantity)       #Create OrderItems
            item.save()                                                                                                            #This copies cart data into order items table.
            item.product.stock -=item.quantity
            item.product.save()
        c.delete()  #Clear Cart


        return render(request,'paymentsuccess.html')


@method_decorator(login_required,name="dispatch")
class OrderSummary(View):  #To add items to Cart Table
    def get(self, request):
        o=Order.objects.filter(user=request.user, is_ordered=True)
        context={'orders':o}

        return render(request,"order_summary.html",context)