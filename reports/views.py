import csv
from django.http import HttpResponse
from django.db.models import Sum, F
from reports.models import OrderItem


def get_order_totals(request):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="order_prices.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(['id', 'total'])

    # get list of orders with their total
    result = OrderItem.objects.values('order_id').order_by('order_id').\
        annotate(total=Sum(F('product__cost') * F('quantity')))
    # build required output (order.id, order total)
    for i in result:
        writer.writerow([i['order_id'], str(i['total'])])
    return response


def get_clients_by_product(request):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="product_customers.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(['id', 'customer_ids'])

    # get list of customers who buy a product (product.id, customer.id)
    result = OrderItem.objects.values("product_id", "order__customer__id").\
        order_by("product_id", "order__customer__id")
    # build required output (product.id, list of customer.id)
    prod = '0'
    cust_list = ''
    for i in result:
        if i['product_id'] != prod:
            writer.writerow([prod, cust_list])
            prod = i['product_id']
            cust_list = ''
        cust_list = cust_list + i['order__customer__id'] + " "
    writer.writerow([prod, cust_list])
    return response


def get_customer_rank(request):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="customer_ranking.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(['id', 'name', 'lastname', 'total'])
    return response
