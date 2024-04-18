from django.urls import path
from . import views

app_name = "intro"

urlpatterns = [
    path('', views.intro, name='intro'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('products/<str:category>/', views.items_category, name='products'),
    path('product/<int:id>/', views.item, name='product'),
    path('logout/', views.logout_view, name='logout'),
    path('user/', views.buyer_user, name='user'),
    path('user/update/', views.update_password_buyer, name='update_password_buyer'),
    path('admin_view/', views.admin_view, name='admin_view'),
    path('create_employee/', views.create_employee, name='create_employee'),
    path('delete_employee/<int:id>/', views.delete_employee, name='delete_employee'),
    path('delete_product/<int:id>/', views.delete_product, name='delete_product'),
    path('look_clients/', views.look_clients, name='look_clients'),
    path('comment/<int:product_id>/', views.comment, name='comment'),
    path('favorite/<int:product_id>/', views.set_favorite_item, name='set_favorite_item'),
    path('delete_favorite/<int:product_id>/', views.delete_favorite_item, name='delete_favorite_item'),
    path('favorite/', views.favorite_items, name='favorite'),
]