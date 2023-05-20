from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


# Create your models here.

class Catagory(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return str(self.name)


class Product(models.Model):
    name = models.CharField(max_length=15)
    pic = models.ImageField(upload_to='Prod_pic/', null=True, blank=True)
    catagory = models.ForeignKey(Catagory, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.FloatField()
    stock = models.PositiveIntegerField()
    discount_price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.name)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.user)

    def total_price(self):
        return self.quantity * self.product.price
