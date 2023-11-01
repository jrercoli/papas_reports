from csv import DictReader
from .models import Customer, Product, Order, OrderItem


def import_customers(data):
    # delete previous data in model
    Customer.objects.all().delete()
    # convert csv data to dict, iterate and create new data in model
    for row in DictReader(data):
        try:
            obj = Customer(id=row['id'], first_name=row['firstname'],
                           last_name=row['lastname'])
            obj.save()
        except:
            raise Exception('Could not import Customers data!')
    return


def import_products(data):
    # delete previous data in model
    Product.objects.all().delete()
    # convert csv data to dict, iterate and create new data in model
    for row in DictReader(data):
        try:
            obj = Product(id=row['id'], name=row['name'], cost=row['cost'])
            obj.save()
        except:
            raise Exception('Could not import Products data!')
    return


def import_orders(data):
    # delete previous data in model
    Order.objects.all().delete()
    # convert csv data to dict, iterate and create new data in model
    for row in DictReader(data):
        try:
            customer = Customer.objects.get(pk=row['customer'])
            order = Order(id=row['id'], customer=customer)
            order.save()
            # split order items string, sort, iterate and create order items model
            product_list = sorted(row['products'].split(" "))
            prod = product_list[0]
            quant = 0
            for i in product_list:
                if prod != i:
                    # save order item and quantity
                    product = Product.objects.get(pk=prod)
                    order_item = OrderItem(order=order, product=product,
                                           quantity=quant)
                    order_item.save()
                    prod = i
                    quant = 0
                quant = quant + 1
            # the last will be save !! ERROR HERE ###########
            product = Product.objects.get(pk=prod)
            order_item = OrderItem(order=order, product=product,
                                    quantity=quant)
            order_item.save()
        except:
            raise Exception('Could not import Orders data!')
    return
