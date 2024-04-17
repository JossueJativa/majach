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
    date = models.DateTimeField(auto_now_add=True)

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()
    stock = models.IntegerField()
    description = models.TextField()
    photo = models.ImageField(upload_to='products/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    stars = models.FloatField(null=True, blank=True, default=0.0)
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
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code_seller = models.CharField(max_length=10, unique=True)

class ClientSellerRelation(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)

# Creacion de ventas
class Sale(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField()
    total = models.FloatField()