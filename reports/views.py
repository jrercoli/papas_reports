from csv import writer
from io import TextIOWrapper

from django.http import HttpResponse
from django.db.models import Sum, F
from django.shortcuts import render
from django.views.generic.base import View
from django.contrib import messages

from .models import OrderItem
from .forms import UploadDataForm
from .views_import_data import import_customers, import_products, import_orders


class UploadDataView(View):

    def get(self, request, *args, **kwargs):
        return render(request, "upload_data.html", {"form": UploadDataForm()})

    def post(self, request, *args, **kwargs):
        customers_file = request.FILES["customers_file"]
        products_file = request.FILES["products_file"]
        orders_file = request.FILES["orders_file"]
        # convert a byte stream to a text stream
        customers_rows = TextIOWrapper(customers_file, encoding="utf-8", newline="")
        products_rows = TextIOWrapper(products_file, encoding="utf-8", newline="")
        orders_rows = TextIOWrapper(orders_file, encoding="utf-8", newline="")
        # import external data to models
        try:
            import_customers(customers_rows)
        except Exception as e:
            messages.error(request, str(e))

        try:
            import_products(products_rows)
        except Exception as e:
            messages.error(request, str(e))

        try:
            import_orders(orders_rows)
        except Exception as e:
            messages.error(request, str(e))

        return render(request, "upload_data.html", {"form": UploadDataForm()})


def get_order_totals(request):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="order_prices.csv"'},
    )

    fwriter = writer(response)
    fwriter.writerow(['id', 'total'])

    # get list of orders with their total
    result = OrderItem.objects.values('order_id').order_by('order_id').\
        annotate(total=Sum(F('product__cost') * F('quantity')))
    # build required output (order.id, order total)
    for i in result:
        fwriter.writerow([i['order_id'], str(round(i['total'], 2))])
    return response


def get_clients_by_product(request):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="product_customers.csv"'},
    )

    fwriter = writer(response)
    fwriter.writerow(['id', 'customer_ids'])

    # get list of customers who buy a product (product.id, customer.id)
    result = OrderItem.objects.values("product_id", "order__customer__id").\
        order_by("product_id", "order__customer__id")
    # build required output (product.id, list of customer.id)
    prod = '0'
    cust_list = ''
    for i in result:
        if i['product_id'] != prod:
            fwriter.writerow([prod, cust_list])
            prod = i['product_id']
            cust_list = ''
        cust_list = cust_list + i['order__customer__id'] + " "
    fwriter.writerow([prod, cust_list])
    return response


def get_customer_rank(request):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="customer_ranking.csv"'},
    )

    fwriter = writer(response)
    fwriter.writerow(['id', 'name', 'lastname', 'total'])

    # get ranking of total purchases per customer
    result = OrderItem.objects.values('order__customer__id',
                                      'order__customer__first_name',
                                      'order__customer__last_name').\
        order_by('order__customer__id').\
        annotate(total=Sum(F('product__cost') * F('quantity')))
    customer_rank = sorted(result, key=lambda x: x['total'], reverse=True)
    # build required output (customer.id, customer.first_name, customer.last_name, total purchases)
    for i in customer_rank:
        fwriter.writerow([i['order__customer__id'], i['order__customer__first_name'],
                         i['order__customer__last_name'], str(round(i['total'], 2))])

    return response
