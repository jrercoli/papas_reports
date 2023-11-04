from csv import DictReader
from collections import Counter
from .models import Customer, Product, Order, OrderItem


def import_customers(data):
    # check data header
    header = next(data)
    if header != 'id,firstname,lastname\r\n':
        raise Exception('Unexpected Customer data header, should be "id, firstname, lastname"')
    data.seek(0)
    # delete previous data in model
    Customer.objects.all().delete()
    # convert csv data to dict, iterate Customers and create new model obj
    for row in DictReader(data):
        try:
            obj = Customer(id=row['id'], first_name=row['firstname'],
                           last_name=row['lastname'])
            obj.save()
        except:
            raise Exception('Could not import Customers data!')
    return


def import_products(data):
    # check data header
    header = next(data)
    if header != 'id,name,cost\r\n':
        raise Exception('Unexpected Product data header, should be "id,name,cost"')
    data.seek(0)
    # delete previous data in model
    Product.objects.all().delete()
    # convert csv data to dict, iterate Products and create new model obj
    for row in DictReader(data):
        try:
            obj = Product(id=row['id'], name=row['name'], cost=row['cost'])
            obj.save()
        except:
            raise Exception('Could not import Products data!')
    return


def import_orders(data):
    # check data header
    header = next(data)
    if header != 'id,customer,products\r\n':
        raise Exception('Unexpected Order data header, should be "id,customer,products"')
    data.seek(0)
    # delete previous data in model
    Order.objects.all().delete()
    # convert csv data to dict, iterate Orders and create new model objs
    for row in DictReader(data):
        try:
            customer = Customer.objects.get(pk=row['customer'])
            order = Order(id=row['id'], customer=customer)
            order.save()
            # split order product items str, count items, create order items
            order_product_list = Counter(row['products'].split(" "))
            for i in order_product_list:
                product = Product.objects.get(pk=str(i))
                order_item = OrderItem(order=order, product=product,
                                       quantity=order_product_list[i])
                order_item.save()
        except:
            raise Exception('Could not import Orders data!')
    return
