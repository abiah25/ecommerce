from django.db import models
from django.contrib.auth.models import User
from shop.models import Product

# Create your models here.

class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)


    def subtotal(self):
        return self.quantity*self.product.price

    def __str__(self):
        return self.user.username


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount=models.IntegerField()
    order_id=models.CharField(max_length=200,null=True)
    ordered_date=models.DateTimeField(auto_now_add=True)
    payment_method=models.CharField(max_length=200)
    address=models.TextField()
    phone=models.CharField(max_length=200)
    is_ordered=models.BooleanField(default=False)
    delivery_status=models.CharField(default="Pending",max_length=200)

    def __str__(self):
        return self.order_id

class OrderItems(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name="products")
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField()

    def __str__(self):
        return self.order.order_id



