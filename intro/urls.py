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
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('favorite/<int:product_id>/', views.set_favorite_item, name='set_favorite_item'),
    path('delete_favorite/<int:product_id>/', views.delete_favorite_item, name='delete_favorite_item'),
    path('favorite/', views.favorite_items, name='favorite'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('delete_cart/<int:product_id>/', views.delete_cart, name='delete_cart'),
    path('add_one_product/<int:product_id>/', views.add_one_product, name='add_one_product'),
    path('remove_one_product/<int:product_id>/', views.remove_one_product, name='remove_one_product'),
    path('complete_buy/', views.complete_buy, name='complete_buy'),
    path('accept_sale/<int:id>/<str:text>/', views.accept_sale, name='accept_sale'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('forgot_username/', views.forgot_username, name='forgot_username'),
    path('stadistics_admin/', views.stadistics_admin, name='stadistics_admin'),
    path('search/', views.search_view, name='search')
]