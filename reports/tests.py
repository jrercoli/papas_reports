import os
from django.test import TestCase
from django.test import Client
from reports.models import Customer, Product, Order,\
                            OrderItem
from reports.views_import_data import import_customers, import_products,\
                               import_orders
from reports.utils import string_to_csv


class ApiStatusOkTest(TestCase):
    def setUp(self):
        # Arrange
        self.client = Client()

    def test_upload_data(self):
        # Act
        response = self.client.get('/upload_data/')
        # Assert
        self.assertEqual(response.status_code, 200)

    def test_status_200_order_totals(self):
        # Act
        response = self.client.get('/api/v1/reports/order_totals/')
        # Assert
        self.assertEqual(response.status_code, 200)

    def test_status_200_customers_product(self):
        # Act
        response = self.client.get('/api/v1/reports/customers_product/')
        # Assert
        self.assertEqual(response.status_code, 200)

    def test_status_200_customer_rank(self):
        # Act
        response = self.client.get('/api/v1/reports/customer_rank/')
        # Assert
        self.assertEqual(response.status_code, 200)


class ApiDownloadDataTest(TestCase):
    def setUp(self):
        # Arrange
        self.client = Client()
        # create some model objs to test csv reports download
        c1 = Customer(id='7', first_name='Roger', last_name='Federer')
        c1.save()
        c2 = Customer(id='11', first_name='Rafa', last_name='Nadal')
        c2.save()
        p1 = Product(id='0', name='Nike T1', cost=15.20)
        p1.save()
        p2 = Product(id='1', name='Puma F5', cost=12.10)
        p2.save()
        p3 = Product(id='5', name='Asus M4', cost=10.50)
        p3.save()
        o1 = Order(id='0', customer=c1)
        o1.save()
        o2 = Order(id='1', customer=c2)
        o2.save()
        o3 = Order(id='2', customer=c1)
        o3.save()
        OrderItem.objects.bulk_create([
            OrderItem(order=o1, product=p2, quantity=2),
            OrderItem(order=o2, product=p1, quantity=1),
            OrderItem(order=o2, product=p3, quantity=1),
            OrderItem(order=o3, product=p1, quantity=1),
            OrderItem(order=o3, product=p3, quantity=2)
        ])

    def test_download_order_totals(self):
        # Arrange
        result = b'id,total\r\n0,24.20\r\n1,25.70\r\n2,36.20\r\n'
        # Act
        response = self.client.get('/api/v1/reports/order_totals/')
        # Assert
        self.assertEqual(response.content, result)

    def test_download_customers_product(self):
        # Arrange
        result = b'id,customer_ids\r\n0,11 7 \r\n1,7 \r\n5,11 7 \r\n'
        # Act
        response = self.client.get('/api/v1/reports/customers_product/')
        # Assert
        self.assertEqual(response.content, result)

    def test_download_customer_rank(self):
        # Arrange
        result = b'id,name,lastname,total\r\n7,Roger,Federer,60.40\r\n11,Rafa,Nadal,25.70\r\n'
        # Act
        response = self.client.get('/api/v1/reports/customer_rank/')
        # Assert
        self.assertEqual(response.content, result)


class ApiImportDataTest(TestCase):
    def test_import_customer(self):
        # Arrange
        # build ext csv file
        s = 'id,firstname,lastname\n7,Roger,Federer\n11,Rafa,Nadal\n'
        f = 'customers.csv'
        _ = string_to_csv(s, f)
        file = open(f, 'r', newline='')
        # target object
        result = Customer(id='11', first_name='Rafa', last_name='Nadal')
        # Act
        import_customers(file)
        os.remove('customers.csv')
        c = Customer.objects.get(pk='11')
        # Assert
        self.assertEqual(c.last_name, result.last_name)

    def test_import_product(self):
        # Arrange
        # build ext csv file
        s = 'id,name,cost\n0,Nike T1,15.20\n1,Puma F5,12.10\n'
        f = 'products.csv'
        _ = string_to_csv(s, f)
        file = open(f, 'r', newline='')        
        # target object
        result = Product(id='1', name='Puma F5', cost=12.10)
        # Act
        import_products(file)
        os.remove('products.csv')
        p = Product.objects.get(pk='1')
        # Assert
        self.assertEqual(p.name, result.name)

    def test_import_order(self):
        # Arrange
        # pre save customer and products
        c2 = Customer(id='11', first_name='Rafa', last_name='Nadal')
        c2.save()
        p1 = Product(id='0', name='Nike T1', cost=15.20)
        p1.save()
        p3 = Product(id='5', name='Asus M4', cost=10.50)
        p3.save()
        # build ext csv file
        s = 'id,customer,products\n1,11,0 5\n'
        f = 'orders.csv'
        _ = string_to_csv(s, f)
        file = open(f, 'r', newline='')
        # target objects
        oresult = Order(id='1', customer=c2)
        iresult = OrderItem(order=oresult, product=p3, quantity=1)
        # Act
        import_orders(file)
        os.remove('orders.csv')
        o = Order.objects.get(pk='1')
        i = OrderItem.objects.get(order=o, product=p3)
        # Assert
        self.assertEqual(o.id, oresult.id)
        self.assertEqual(i.product.name, iresult.product.name)
