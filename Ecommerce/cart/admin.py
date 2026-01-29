from django.contrib import admin
from cart.models import Cart,Order,OrderItems
# Register your models here.

admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItems)
