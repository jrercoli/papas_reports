from django.contrib import admin
from reports.models import Product, Customer, Order, OrderItem


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
