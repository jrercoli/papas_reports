from django.contrib import admin
from reports.models import Product, Customer, Order, OrderItem


admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
