from django.urls import path
from reports import views

urlpatterns = [
    path('reports/order_totals/', views.get_order_totals,
         name="get-order-totals"),
    path('reports/customers_product/', views.get_clients_by_product,
         name="get-customers-product"),
    path('reports/customer_rank/', views.get_customer_rank,
         name="get-customer-rank"),
]
