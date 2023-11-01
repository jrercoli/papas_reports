from django.forms import FileField, Form


class UploadDataForm(Form):
    customers_file = FileField()
    products_file = FileField()
    orders_file = FileField()
