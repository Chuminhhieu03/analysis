from django.db import models
from django.contrib.auth.models import User
from category.models import Category
# from order.models import OrderDetail

# Create your models here.
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name + ' - ' + str(self.price)
    
    # def get_total_revenue(self):
    #     order_details = OrderDetail.objects.filter(product=self, order__status=2)
    #     total_revenue = sum([od.total for od in order_details])
    #     return total_revenue

      