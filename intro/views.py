from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Client, Category, Product, Seller
import random
import string

def login_view(request):
    session = request.session.get('redirect_to')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Autenticar el usuario
        try:
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                if session == 'register.html':
                    session = 'intro.html'

                return render(request, session or 'intro.html')
            else:
                return render(request, session or 'intro.html', {'error': 'Usuario o contraseña incorrectos'})
        except:
            return render(request, session or 'intro.html', {'error': 'Usuario o contraseña incorrectos'})
        
def intro(request):
    request.session['redirect_to'] = 'intro.html'
    return render(request, 'intro.html')

def items_category(request, category):
    products = Product.objects.filter(category=Category.objects.get(name=category))
    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(products, 100)
        products = paginator.page(page)
    except:
        paginator = Paginator(products, 1)
        products = paginator.page(1)

    return render(request, 'items_category.html', {
        'entity': products,
        'paginator': paginator
    })

def item(request, id):
    product = Product.objects.get(pk=id)
    return render(request, 'item.html', {
        'product': product
    })

def register(request):
    if request.user.is_authenticated:
        return render(request, 'intro.html', {
            'error': 'Ya has iniciado sesión'
        })
    request.session['redirect_to'] = 'register.html'
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        phone = request.POST.get('phone')

        if password == password2:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                phone=phone
            )
            user.save()

            client = Client(user=user)
            client.save()

            user = authenticate(username=username, password=password)
            login(request, user)
            return render(request, 'intro.html')
        else:
            return render(request, 'register.html', {
                'error': 'Las contraseñas no coinciden',
                'username': username,
                'email': email,
                'phone': phone
            })
    return render(request, 'register.html')

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return render(request, 'intro.html')
    else:
        return render(request, 'intro.html', {
            'error': 'Debes iniciar sesión para acceder a esta página'
        })

def buyer_user(request):
    if request.user.is_authenticated:
        request.session['redirect_to'] = 'users/buyer_user.html'
        if request.method == 'POST':
            user = User.objects.get(pk=request.user.id)
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.username = request.POST.get('username')
            user.phone = request.POST.get('phone')
            user.save()
            client = Client.objects.get(user=user)
            client.principal_address = request.POST.get('principal_address')
            client.secondary_address = request.POST.get('secondary_address')
            client.no_house = request.POST.get('no_house')
            client.save()
            return render(request, 'users/buyer_user.html', {
                'success': 'Usuario actualizado correctamente',
            })
        else:
            if request.user.is_admin or request.user.is_seller:
                return render(request, 'users/buyer_user.html')
            else:
                return render(request, 'users/buyer_user.html', {
                    'client': Client.objects.get(user=request.user)
                })
    else:
        return render(request, 'intro.html', {
            'error': 'Debes iniciar sesión para acceder a esta página'
        })
    
def update_password_buyer(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = User.objects.get(pk=request.user.id)
            if not user.check_password(request.POST.get('password')):
                return render(request, 'users/buyer_user.html', {
                    'error': 'La contraseña actual no es correcta'
                })
            
            password = request.POST.get('password_change')
            password2 = request.POST.get('password_change2')
            if password == password2:
                user.set_password(password)
                user.save()
                logout(request)
                return render(request, 'intro.html', {
                    'success': 'Contraseña actualizada correctamente'
                })
            else:
                return render(request, 'users/buyer_user.html', {
                    'error': 'Las contraseñas no coinciden'
                })
    else:
        return render(request, 'intro.html', {
            'error': 'Debes iniciar sesión para acceder a esta página'
        })
    
def admin_view(request):
    if request.user.is_authenticated and request.user.is_admin:
        if request.method == 'POST':
            id = request.POST.get('id_product')
            name = request.POST.get('name')
            price = request.POST.get('price')
            stock = request.POST.get('stock')
            description = request.POST.get('description')
            category = request.POST.get('category')
            photo = request.FILES.get('photo')

            if id:
                product = Product.objects.get(pk=id)
                product.name = name
                product.price = price
                product.stock = stock
                
                if description:
                    product.description = description

                if int(category) > 0:
                    product.category = Category.objects.get(pk=category)

                if photo:
                    product.photo = photo

                product.save()
                return render(request, 'users/admin.html', {
                    'success': 'Producto editado correctamente',
                    'sellers': Seller.objects.all(),
                    'categories': Category.objects.all(),
                    'products': Product.objects.all()
                })
            else:
                if category == 0:
                    return render(request, 'users/admin.html', {
                        'error': 'Debes seleccionar una categoría',
                        'sellers': Seller.objects.all(),
                        'categories': Category.objects.all(),
                        'products': Product.objects.all()
                    })
                
                product = Product(
                    name=name,
                    price=price,
                    stock=stock,
                    description=description,
                    category=Category.objects.get(pk=category),
                    photo=photo
                )
                product.save()
                return render(request, 'users/admin.html', {
                    'success': 'Producto creado correctamente',
                    'sellers': Seller.objects.all(),
                    'categories': Category.objects.all(),
                    'products': Product.objects.all()
                })
        else:
            return render(request, 'users/admin.html', {
                'sellers': Seller.objects.all(),
                'categories': Category.objects.all(),
                'products': Product.objects.all()
            })
    else:
        return render(request, 'intro.html', {
            'error': 'Debes iniciar sesión como administrador para acceder a esta página'
        })
    
def create_employee(request):
    if request.user.is_authenticated and request.user.is_admin:
        if request.method == 'POST':
            id = request.POST.get('id')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password2 = request.POST.get('password2')
            phone = request.POST.get('phone')
            photo = request.FILES.get('photo')
            if id:
                seller = Seller.objects.get(pk=id)
                if password != '':
                    if password == password2:
                        seller.user.set_password(password)

                seller.user.username = username
                seller.user.email = email
                seller.user.phone = phone
                seller.user.first_name = first_name
                seller.user.last_name = last_name
                if photo:
                    seller.user.photo = seller.user.photo
                seller.user.save()
                return render(request, 'users/admin.html', {
                    'success': 'Empleado editado correctamente',
                    'sellers': Seller.objects.all()
                })
            else:
                if not photo:
                    photo = 'default.png'

                if password == password2:
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password,
                        phone=phone,
                        photo=photo
                    )
                    user.first_name = first_name
                    user.last_name = last_name
                    user.is_seller = True
                    user.save()

                    seller = Seller(user=user)                
                    code = ''.join(random.choices(string.ascii_uppercase, k=2)) + ''.join(random.choices(string.digits, k=4))
                    seller.code_seller = code
                    seller.save()

                    return render(request, 'users/admin.html', {
                        'success': 'Empleado creado correctamente',
                        'sellers': Seller.objects.all()
                    })
                
                else:
                    return render(request, 'users/admin.html', {
                        'error': 'Las contraseñas no coinciden',
                        'first_name': first_name,
                        'last_name': last_name,
                        'username': username,
                        'email': email,
                        'phone': phone,
                        'sellers': Seller.objects.all()
                    })
        else:
            return render(request, 'users/admin.html', {
                'sellers': Seller.objects.all()
            })
    else:
        return render(request, 'intro.html', {
            'error': 'Debes iniciar sesión como administrador para acceder a esta página'
        })
    
def delete_employee(request, id):
    if request.user.is_authenticated and request.user.is_admin:
        seller = Seller.objects.get(pk=id)
        user = User.objects.get(pk=seller.user.id)
        user.delete()
        return render(request, 'users/admin.html', {
            'success': 'Empleado eliminado correctamente',
            'sellers': Seller.objects.all()
        })
    else:
        return render(request, 'intro.html', {
            'error': 'Debes iniciar sesión como administrador para acceder a esta página'
        })
    
def delete_product(request, id):
    if request.user.is_authenticated and request.user.is_admin:
        product = Product.objects.get(pk=id)
        product.delete()
        return render(request, 'users/admin.html', {
            'success': 'Producto eliminado correctamente',
            'sellers': Seller.objects.all(),
            'categories': Category.objects.all(),
            'products': Product.objects.all()
        })
    else:
        return render(request, 'intro.html', {
            'error': 'Debes iniciar sesión como administrador para acceder a esta página'
        })
    
def look_clients(request):
    if request.user.is_authenticated and request.user.is_seller:
        employee = Seller.objects.get(user=request.user)
        clients = Client.objects.filter(clientsellerrelation__seller=employee)
        return render(request, 'users/employee.html', {
            'employee': employee,
            'clients': clients
        })
    else:
        return render(request, 'intro.html', {
            'error': 'Debes iniciar sesión como administrador para acceder a esta página'
        })