from django.db import models


class Customer(models.Model):
    id = models.CharField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)


class Product(models.Model):
    id = models.CharField(primary_key=True)
    name = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=8, decimal_places=2)


class Order(models.Model):
    id = models.CharField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
