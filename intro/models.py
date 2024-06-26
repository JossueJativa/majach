from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    phone = models.CharField(max_length=10)
    photo = models.ImageField(upload_to='users/', default='users/default.png')
    is_admin = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)

    def photo_url(self):
        if self.photo:
            return self.photo.url
        return None
    
class Category(models.Model):
    name = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='categories/', default='categories/default-category.jpeg')

    def photo_url(self):
        if self.photo:
            return self.photo.url
        return None
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    stars = models.FloatField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()
    stock = models.IntegerField()
    description = models.TextField()
    photo = models.ImageField(upload_to='products/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    comments = models.ManyToManyField(Comment, blank=True)

    def photo_url(self):
        if self.photo:
            return self.photo.url
        return None
    
class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    principal_address = models.CharField(max_length=100, null=True)
    secondary_address = models.CharField(max_length=100, null=True)
    no_house = models.CharField(max_length=10)

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code_seller = models.CharField(max_length=10, unique=True)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField()

class Product_Quantity(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

class ClientSellerRelation(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    done_sale = models.BooleanField(default=False)
    Product_Quantity = models.ManyToManyField(Product_Quantity)
    is_delivered = models.BooleanField(default=False)
    total = models.FloatField()

class Sale(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    Product_Quantity = models.ManyToManyField(Product_Quantity, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    total = models.FloatField()