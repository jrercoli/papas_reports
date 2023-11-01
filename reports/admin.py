from django.contrib import admin
from reports.models import Product, Customer, Order, OrderItem


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name')


admin.site.register(Product)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
