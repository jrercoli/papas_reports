from django.test import TestCase
from django.test import Client
from reports.models import Customer, Product, Order,\
                            OrderItem


class ApiStatusOkTest(TestCase):
    def setUp(self):
        # arrange
        self.client = Client()

    def test_upload_data(self):
        # act
        response = self.client.get('/upload_data/')
        # assert
        self.assertEqual(response.status_code, 200)

    def test_status_200_order_totals(self):
        # act
        response = self.client.get('/api/v1/reports/order_totals/')
        # assert
        self.assertEqual(response.status_code, 200)

    def test_status_200_customers_product(self):
        # act
        response = self.client.get('/api/v1/reports/customers_product/')
        # assert
        self.assertEqual(response.status_code, 200)

    def test_status_200_customer_rank(self):
        # act
        response = self.client.get('/api/v1/reports/customer_rank/')
        # assert
        self.assertEqual(response.status_code, 200)


class ApiDownloadDataTest(TestCase):
    def setUp(self):
        # arrange
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
        # arrange
        result = b'id,total\r\n0,24.20\r\n1,25.70\r\n2,36.20\r\n'
        # act
        response = self.client.get('/api/v1/reports/order_totals/')
        # assert
        self.assertEqual(response.content, result)

    def test_download_customers_product(self):
        # arrange
        result = b'id,customer_ids\r\n0,11 7 \r\n1,7 \r\n5,11 7 \r\n'
        # act
        response = self.client.get('/api/v1/reports/customers_product/')
        # assert
        self.assertEqual(response.content, result)

    def test_download_customer_rank(self):
        # arrange
        result = b'id,name,lastname,total\r\n7,Roger,Federer,60.40\r\n11,Rafa,Nadal,25.70\r\n'
        # act
        response = self.client.get('/api/v1/reports/customer_rank/')
        # assert
        self.assertEqual(response.content, result)

