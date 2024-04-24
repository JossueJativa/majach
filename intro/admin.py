from django.contrib import admin
from .models import ClientSellerRelation, Product_Quantity, Sale, User, Client, Category, Product, Seller, Comment, Favorite, Cart

# Register your models here.
admin.site.register(ClientSellerRelation)
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Client)
admin.site.register(Seller)
admin.site.register(Comment)
admin.site.register(Favorite)
admin.site.register(Cart)
admin.site.register(Sale)
admin.site.register(Product_Quantity)
