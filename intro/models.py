from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.CharField(max_length=10)
    photo = models.ImageField(upload_to='users/', default='users/default.png')
    is_admin = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)

    def photo_url(self):
        if self.photo:
            return self.photo.url
        return None

class UserBuilder:
    def __init__(self):
        self.user = User()

    def with_username(self, username):
        self.user.username = username
        return self

    def with_email(self, email):
        self.user.email = email
        return self

    def with_phone(self, phone):
        self.user.phone = phone
        return self

    def with_photo(self, photo):
        self.user.photo = photo
        return self

    def as_admin(self):
        self.user.is_admin = True
        return self

    def as_seller(self):
        self.user.is_seller = True
        return self
    
    def with_password(self, password):
        self.user.set_password(password)
        return self

    def build(self):
        self.user.save()
        return self.user
    
class Category(models.Model):
    name = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='categories/', default='categories/default-category.jpeg')

    def photo_url(self):
        if self.photo:
            return self.photo.url
        return None

class CategoryBuilder:
    def __init__(self):
        self.category = Category()

    def with_name(self, name):
        self.category.name = name
        return self

    def with_photo(self, photo):
        self.category.photo = photo
        return self

    def build(self):
        self.category.save()
        return self.category
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    stars = models.FloatField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def get_stars(self):
        if self.stars:
            return self.stars
        return None
    
class CommentBuilder:
    def __init__(self):
        self.comment = Comment()

    def with_user(self, user):
        self.comment.user = user
        return self

    def with_comment(self, comment):
        self.comment.comment = comment
        return self

    def with_stars(self, stars):
        self.comment.stars = stars
        return self

    def build(self):
        self.comment.save()
        return self.comment

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

class ProductBuilder:
    def __init__(self):
        self.product = Product()

    def with_name(self, name):
        self.product.name = name
        return self

    def with_price(self, price):
        self.product.price = price
        return self

    def with_stock(self, stock):
        self.product.stock = stock
        return self

    def with_description(self, description):
        self.product.description = description
        return self

    def with_photo(self, photo):
        self.product.photo = photo
        return self

    def with_category(self, category):
        self.product.category = category
        return self

    def build(self):
        self.product.save()
        return self.product
    
class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    principal_address = models.CharField(max_length=100, null=True)
    secondary_address = models.CharField(max_length=100, null=True)
    no_house = models.CharField(max_length=10)
    category = models.CharField(max_length=50, default='Sin Clasificar')

class ClientBuilder:
    def __init__(self):
        self.client = Client()

    def with_user(self, user):
        self.client.user = user
        return self

    def with_principal_address(self, principal_address):
        self.client.principal_address = principal_address
        return self

    def with_secondary_address(self, secondary_address):
        self.client.secondary_address = secondary_address
        return self

    def with_no_house(self, no_house):
        self.client.no_house = no_house
        return self

    def with_category(self, category):
        self.client.category = category
        return self

    def build(self):
        self.client.save()
        return self.client

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)

class FavoriteBuilder:
    def __init__(self):
        self.favorite = Favorite()

    def with_user(self, user):
        self.favorite.user = user
        return self

    def with_product(self, product):
        self.favorite.product = product
        return self

    def build(self):
        self.favorite.save()
        return self.favorite

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code_seller = models.CharField(max_length=10, unique=True)

class SellerBuilder:
    def __init__(self):
        self.seller = Seller()

    def with_user(self, user):
        self.seller.user = user
        return self

    def with_code_seller(self, code_seller):
        self.seller.code_seller = code_seller
        return self

    def build(self):
        self.seller.save()
        return self.seller

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField()

class CartBuilder:
    def __init__(self):
        self.cart = Cart()

    def with_user(self, user):
        self.cart.user = user
        return self

    def with_product(self, product):
        self.cart.product = product
        return self

    def with_quantity(self, quantity):
        self.cart.quantity = quantity
        return self

    def build(self):
        self.cart.save()
        return self.cart

class Product_Quantity(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

class Product_QuantityBuilder:
    def __init__(self):
        self.product_quantity = Product_Quantity()

    def with_product(self, product):
        self.product_quantity.product = product
        return self

    def with_quantity(self, quantity):
        self.product_quantity.quantity = quantity
        return self

    def build(self):
        self.product_quantity.save()
        return self.product_quantity

class ClientSellerRelation(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    done_sale = models.BooleanField(default=False)
    Product_Quantity = models.ManyToManyField(Product_Quantity)
    is_delivered = models.BooleanField(default=False)
    total = models.FloatField()

class ClientSellerRelationBuilder:
    def __init__(self):
        self.client_seller_relation = ClientSellerRelation()

    def with_client(self, client):
        self.client_seller_relation.client = client
        return self

    def with_seller(self, seller):
        self.client_seller_relation.seller = seller
        return self

    def with_done_sale(self, done_sale):
        self.client_seller_relation.done_sale = done_sale
        return self

    def with_product_quantity(self, product_quantity):
        self.client_seller_relation.Product_Quantity.add(product_quantity)
        return self

    def with_is_delivered(self, is_delivered):
        self.client_seller_relation.is_delivered = is_delivered
        return self

    def with_total(self, total):
        self.client_seller_relation.total = total
        return self

    def build(self):
        self.client_seller_relation.save()
        return self.client_seller_relation

class Sale(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    Product_Quantity = models.ManyToManyField(Product_Quantity, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    total = models.FloatField()

class SaleBuilder:
    def __init__(self):
        self.sale = Sale()

    def with_client(self, client):
        self.sale.client = client
        return self

    def with_product_quantity(self, product_quantity):
        self.sale.Product_Quantity.add(product_quantity)
        return self

    def with_total(self, total):
        self.sale.total = total
        return self

    def build(self):
        self.sale.save()
        return self.sale