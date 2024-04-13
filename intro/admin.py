from django.contrib import admin
from .models import User, Category, Product, Client, Seller

# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Client)
admin.site.register(Seller)