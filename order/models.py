from django.db import models
from django.contrib.auth.models import User
from customer.models import Customer
from product.models import Product
# Create your models here.

STATUS_CHOICES = (
    ('0', 'Vừa mới tạo đơn hàng'),
    ('1', 'Đang giao hàng'),
    ('2', 'Đã giao hàng thành công'),
    ('3', 'Đã hủy')
)


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100, default="")
    create_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    total = models.FloatField(default=0)
    discrption = models.TextField(default="")
    status = models.CharField(
        max_length=100, choices=STATUS_CHOICES, default='0')
    
    def __str__(self):
        return str(self.id) + " - " + self.customer_name + " - " + str(STATUS_CHOICES[int(self.status)][1])
    
class OrderDetail(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100, default="")
    product_price = models.FloatField(default=0)
    quantity = models.IntegerField(default=0)
    total = models.FloatField(default=0)
    
    def __str__(self):
        return str(self.id) + " - " + self.product.name + " - " + str(self.quantity) + " - " + str(self.total)
