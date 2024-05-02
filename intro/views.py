from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import ClientSellerRelation, Product_Quantity, Sale, User, Client, Category, Product, Seller, Comment, Favorite, Cart
from django.core.mail import send_mail
from django.conf import settings
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
        paginator = Paginator(products, 40)
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

    # Sacar una media de las estrellas
    stars = 0
    for c in product.comments.all():
        stars += c.stars

    try:
        star = stars / product.comments.count()
    except:
        star = 0

    # Quitar los decimales
    star = int(star)

    # Ordenar de mas estrellas a menos estrellas
    comment = product.comments.all().order_by('-stars')

    # Comprobar si el producto está en favoritos
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.id)
        try:
            favorite = Favorite.objects.filter(user=user, product=product)
            if favorite:
                favorite = True
            else:
                favorite = False
        except:
            favorite = False
    else:
        favorite = False

    return render(request, 'item.html', {
        'product': product,
        "comments": comment,
        'star': star,
        'favorite': favorite
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
        clients = ClientSellerRelation.objects.filter(seller=employee)

        # Filtrar por los que no han sido entregados
        # clients = clients.filter(done_sale=False)

        # paginator
        page = request.GET.get('page', 1)
        try:
            paginator = Paginator(clients, 10)
            clients = paginator.page(page)
        except:
            paginator = Paginator(clients, 1)
            clients = paginator.page(1)

        return render(request, 'users/employee.html', {
            'employee': employee,
            'entity': clients,
            'paginator': paginator
        })
    else:
        return render(request, 'intro.html', {
            'error': 'Debes iniciar sesión como administrador para acceder a esta página'
        })
    
def comment(request, product_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            product = Product.objects.get(pk=product_id)
            user = User.objects.get(pk=request.user.id)
            comment = request.POST.get('comment')
            rating = request.POST.get('rating')

            comment = Comment(user=user, comment=comment, stars=rating)
            comment.save()

            product.comments.add(comment)
            product.save()

            # Sacar una media de las estrellas
            stars = 0
            for c in product.comments.all():
                stars += c.stars

            star = stars / product.comments.count()
            # Quitar los decimales
            star = int(star)

            # Ordenar de mas estrellas a menos estrellas
            comment = product.comments.all().order_by('-stars')

            return render(request, 'item.html', {
                'product': product,
                'success': 'Comentario agregado correctamente',
                'comments': comment,
                'star': star
            })
        else:
            return render(request, 'item.html', {
                'product': Product.objects.get(pk=product_id),
                'error': 'Debes iniciar sesión para comentar'
            })
    else:
        product = Product.objects.get(pk=product_id)
        comment = product.comments.all().order_by('-stars')
        return render(request, 'item.html', {
            'product': Product.objects.get(pk=product_id),
            'error': 'Debes iniciar sesión para acceder a esta página',
            'comments': comment
        })   

def delete_comment(request, comment_id):
    if request.method  == 'POST':
        comment = Comment.objects.get(pk=comment_id)
        product = Product.objects.get(comments=comment)
        comment.delete()

        # Sacar una media de las estrellas
        stars = 0
        for c in product.comments.all():
            stars += c.stars

        star = stars / product.comments.count()
        # Quitar los decimales
        star = int(star)

        # Ordenar de mas estrellas a menos estrellas
        comment = product.comments.all().order_by('-stars')

        return render(request, 'item.html', {
            'product': product,
            'success': 'Comentario eliminado correctamente',
            'comments': comment,
            'star': star
        })

    
def set_favorite_item(request, product_id):
    if request.user.is_authenticated:
        product = Product.objects.get(pk=product_id)
        user = User.objects.get(pk=request.user.id)
        favorite = Favorite(user=user, product=product)
        favorite.save()

        # comprobar si el producto está en favoritos
        try:
            favorite = Favorite.objects.filter(user=user, product=product)
            if favorite:
                favorite = True
            else:
                favorite = False
        except:
            favorite = False

        return render(request, 'item.html', {
            'product': product,
            'success': 'Producto añadido a favoritos',
            'favorite': favorite
        })
    else:
        product = Product.objects.get(pk=product_id)
        comment = product.comments.all().order_by('-stars')
        return render(request, 'item.html', {
            'product': Product.objects.get(pk=product_id),
            'error': 'Debes iniciar sesión para agregar a favoritos',
            'comments': comment
        })
    
def delete_favorite_item(request, product_id):
    if request.user.is_authenticated:
        product = Product.objects.get(pk=product_id)
        user = User.objects.get(pk=request.user.id)
        favorite = Favorite.objects.filter(user=user, product=product).first()
        favorite.delete()

        # comprobar si el producto está en favoritos
        try:
            favorite = Favorite.objects.filter(user=user, product=product)
            if favorite:
                favorite = True
            else:
                favorite = False
        except:
            favorite = False

        return render(request, 'item.html', {
            'product': product,
            'success': 'Producto eliminado de favoritos',
            'favorite': favorite
        })
    else:
        product = Product.objects.get(pk=product_id)
        comment = product.comments.all().order_by('-stars')
        return render(request, 'item.html', {
            'product': Product.objects.get(pk=product_id),
            'error': 'Debes iniciar sesión sesión para eliminar de favoritos',
            'comments': comment
        })
    
def favorite_items(request):
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.id)
        favorites = Favorite.objects.filter(user=user)
        return render(request, 'users/favorite.html', {
            'favorites': favorites
        })
    else:
        return render(request, 'intro.html', {
            'error': 'Debes iniciar sesión para acceder a esta página'
        })
    
def cart(request):
    if request.user.is_authenticated:
        try:
            user = User.objects.get(pk=request.user.id)
            code_seller = ClientSellerRelation.objects.filter(client=Client.objects.get(user=user)).first()
            code_seller = code_seller.seller.code_seller
        except:
            code_seller = ""
        
        user = User.objects.get(pk=request.user.id)
        try:
            cart = Cart.objects.filter(user=user)
        except:
            cart = None

        # Calcular el total
        total = 0
        try:
            for c in cart:
                total += c.product.price * c.quantity
        except:
            total = 0

        return render(request, 'users/cart.html', {
            'cart': cart,
            'total': total,
            'code_seller': code_seller
        })
    else:
        return render(request, 'intro.html', {
            'error': 'Debes iniciar sesión para acceder a esta página'
        })
    
def add_to_cart(request, product_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = User.objects.get(pk=request.user.id)
            product = Product.objects.get(pk=product_id)

            # Verificar si el producto ya está en el carrito
            try:
                cart = Cart.objects.get(user=user, product=product)
                if cart.quantity >= cart.product.stock:
                    cart.quantity = cart.product.stock
                    cart.save()
                    return render(request, 'users/cart.html', {
                        'error': 'No hay más stock de este producto',
                        'cart': Cart.objects.filter(user=user)
                    })
                else:
                    cart.quantity += 1
                    cart.save()
            except:
                cart = Cart(user=user, product=product, quantity=1)
                cart.save()

            try:
                user = User.objects.get(pk=request.user.id)
                code_seller = ClientSellerRelation.objects.filter(client=Client.objects.get(user=user)).first()
                code_seller = code_seller.seller.code_seller
            except:
                code_seller = ""

            return render(request, 'users/cart.html', {
                'success': 'Producto añadido al carrito',
                'cart': Cart.objects.filter(user=user),
                'code_seller': code_seller
            })
    else:
        return render(request, 'intro.html', {
            'error': 'Debes iniciar sesión para acceder a esta página'
        })
    
def delete_cart(request, product_id):
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.id)
        try:
            user = User.objects.get(pk=request.user.id)
            code_seller = ClientSellerRelation.objects.filter(client=Client.objects.get(user=user)).first()
            code_seller = code_seller.seller.code_seller
        except:
            code_seller = ""
        try:
            cart = Cart.objects.get(pk=product_id)
            cart.delete()

            return render(request, 'users/cart.html', {
                'success': 'Producto eliminado del carrito',
                'cart': Cart.objects.filter(user=user),
                'code_seller': code_seller
            })
        except:
            return render(request, 'users/cart.html', {
                'error': 'El producto no está en el carrito',
                'cart': Cart.objects.filter(user=user),
                'code_seller': code_seller
            })
    else:
        return render(request, 'intro.html', {
            'error': 'Debes iniciar sesión para acceder a esta página'
        })
    
def add_one_product(request, product_id):
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.id)
        cart = Cart.objects.get(pk=product_id)

        # Añadir uno al producto
        cart.quantity += 1
        cart.save()

        # Verificar si la cantidad del producto es menor o igual al stock
        if cart.quantity >= cart.product.stock:
            cart.quantity = cart.product.stock
            cart.save()

        try:
            cart = Cart.objects.filter(user=user)
        except:
            cart = None

        # Calcular el total
        total = 0
        try:
            for c in cart:
                total += c.product.price * c.quantity
        except:
            total = 0

        return render(request, 'users/cart.html', {
            'success': 'Producto añadido al carrito',
            'cart': Cart.objects.filter(user=user),
            'total': total
        })
    else:
        return render(request, 'intro.html', {
            'error': 'Debes iniciar sesión para acceder a esta página'
        })
    
def remove_one_product(request, product_id):
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.id)
        cart = Cart.objects.get(pk=product_id)
        if cart.quantity > 1:
            cart.quantity -= 1
            cart.save()

            try:
                cart = Cart.objects.filter(user=user)
            except:
                cart = None

            # Calcular el total
            total = 0
            try:
                for c in cart:
                    total += c.product.price * c.quantity
            except:
                total = 0

            return render(request, 'users/cart.html', {
                'success': 'Producto eliminado del carrito',
                'cart': Cart.objects.filter(user=user),
                'total': total
            })
        else:
            cart.delete()
            try:
                cart = Cart.objects.filter(user=user)
            except:
                cart = None

            # Calcular el total
            total = 0
            try:
                for c in cart:
                    total += c.product.price * c.quantity
            except:
                total = 0
                
            return render(request, 'users/cart.html', {
                'success': 'Producto eliminado del carrito',
                'cart': Cart.objects.filter(user=user),
                'total': total
            })
    else:
        return render(request, 'intro.html', {
            'error': 'Debes iniciar sesión para acceder a esta página'
        })
    
def complete_buy(request):
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.id)
        cart = Cart.objects.filter(user=user)
        
        if request.method == 'POST':
            if not cart:
                return render(request, 'intro.html', {
                    'error': 'No tienes productos en el carrito'
                })
            
            # Comprobar si aun hay stock en los productos
            for c in cart:
                if c.quantity > c.product.stock:
                    # Reducir la cantidad al stock
                    c.quantity = c.product.stock
                    c.save()
                    return render(request, 'users/cart.html', {
                        'error': f'Solo hay {c.product.stock} unidades de {c.product.name} en stock',
                        'cart': Cart.objects.filter(user=user)
                    })
            
            user_buyer = request.POST.get('user_buyer')
            is_delivery = request.POST.get('is_delivery')
            if is_delivery == None:
                is_delivery = False
            else:
                is_delivery = True

            if user_buyer == "":
                sellers = Seller.objects.all()
                relation = None
                for s in sellers:
                    if not relation:
                        relation = ClientSellerRelation.objects.filter(seller=s).count()
                        seller = s
                    else:
                        if ClientSellerRelation.objects.filter(seller=s).count() < relation:
                            relation = ClientSellerRelation.objects.filter(seller=s).count()
                            seller = s
            else:
                seller = Seller.objects.get(code_seller=user_buyer)

            # Crear la venta
            total = 0
            for c in cart:
                total += c.product.price * c.quantity
            sale = Sale(client=user, total=total)
            sale.save()

            # Agregar los productos y su cantidad
            for c in cart:
                product_quantity = Product_Quantity(product=c.product, quantity=c.quantity)
                product_quantity.save()
                sale.Product_Quantity.add(product_quantity)
                sale.save()

            # Eliminar el carrito
            cart.delete()

            # Crear la relación de venta
            client = Client.objects.get(user=user)
            relation = ClientSellerRelation(client=client, seller=seller, is_delivered=is_delivery, total=total)
            relation.save()

            for p in sale.Product_Quantity.all():
                relation.Product_Quantity.add(p)
                relation.save()

            # Enviar correo al cliente
            subject = 'Compra realizada'
            message = f'Se ha realizado una compra por un total de {total}$ en la tienda, pronto se comunicara con usted el vendedor'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email]
            send_mail(subject, message, email_from, recipient_list)

        return render(request, 'intro.html', {
            'success': 'Compra realizada correctamente'
        })
    else:
        return render(request, 'intro.html', {
            'error': 'Debes iniciar sesión para acceder a esta página'
        })
    
def accept_sale(request, id, text):
    if request.user.is_authenticated and request.user.is_seller:
        # paginador
        page = request.GET.get('page', 1)
        try:
            paginator = Paginator(ClientSellerRelation.objects.filter(seller=Seller.objects.get(user=request.user), done_sale=False), 10)
            entity = paginator.page(page)
        except:
            paginator = Paginator(ClientSellerRelation.objects.filter(seller=Seller.objects.get(user=request.user), done_sale=False), 1)
            entity = paginator.page(1)
        if (text == "entregado"):
            relation = ClientSellerRelation.objects.get(pk=id)
            relation.done_sale = True
            relation.save()

            # bajar el stock
            for p in relation.Product_Quantity.all():
                product = Product.objects.get(pk=p.product.id)
                product.stock -= p.quantity
                product.save()

            return render(request, 'users/employee.html', {
                'success': 'Venta aceptada correctamente',
                'entity': relation,
                'paginator': paginator
            })

        elif (text == "rechazado"):
            relation = ClientSellerRelation.objects.get(pk=id)
            relation.delete()

            return render(request, 'users/employee.html', {
                'success': 'Venta rechazada correctamente',
                'entity': entity,
                'paginator': paginator
            })
        else:
            return render(request, 'intro.html', {
                'error': 'No puedes acceder a esta página'
            })
    else:
        return render(request, 'intro.html', {
            'error': 'Debes iniciar sesión como empleado para acceder a esta página'
        })
    
def forgot_username(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            # Enviar por correo el nombre de usuario
            subject = 'Recuperación de nombre de usuario'
            message = f'Su nombre de usuario es: {user.username}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, email_from, recipient_list)
            return render(request, 'forgot_username.html', {
                'success': 'Se ha enviado un correo con el nombre de usuario'
            })
        except:
            return render(request, 'forgot_username.html', {
                'error': 'El correo no está registrado'
            })
    return render(request, 'forgot_username.html')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            user.set_password(password)
            user.save()

            # Enviar correo
            subject = 'Recuperación de contraseña'
            message = f'Su nueva contraseña es: {password}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, email_from, recipient_list)

            return render(request, 'forgot_password.html', {
                'success': 'Se ha enviado un correo con la nueva contraseña'
            })
        except:
            return render(request, 'forgot_password.html', {
                'error': 'El correo no está registrado'
            })
    return render(request, 'forgot_password.html')

def search_view(request):
    if request.method == 'POST':
        search_query = request.POST.get('search')
        products = Product.objects.filter(name__icontains=search_query)
        paginator = Paginator(products, 40)  # 10 productos por página

        page_number = request.GET.get('page')
        try:
            products_page = paginator.page(page_number)
        except PageNotAnInteger:
            products_page = paginator.page(1)
        except EmptyPage:
            products_page = paginator.page(paginator.num_pages)

        return render(request, 'search.html', {
            'entity': products_page,
            'namesearch': search_query
        })
    return render(request, 'search.html')

def stadistics_admin(request):
    if request.user.is_authenticated and request.user.is_admin:
        # Ver los productos más vendidos
        try:
            products = Product.objects.all()
            products_sale = {}
            for p in products:
                products_sale[p.name] = 0
                for s in Sale.objects.all():
                    for q in s.Product_Quantity.all():
                        if q.product == p:
                            products_sale[p.name] += q.quantity
        except:
            products_sale = {}



        # Ordenar de mayor a menor
        products_sale = dict(sorted(products_sale.items(), key=lambda item: item[1], reverse=True))
        return render(request, 'users/stadistics_admin.html', {
            'products': products_sale
        })
    else:
        return render(request, 'intro.html', {
            'error': 'Debes iniciar sesión como administrador para acceder a esta página'
        })
    
def get_products(request):
    chart = {
        'tooltip': {
            'trigger': 'item',
        },
        'legend': {
            'orient': 'vertical',
            'left': 'left',
        },
    }
    try:
        products = Product.objects.all()
        products_sale = {}
        for p in products:
            products_sale[p.name] = 0
            for s in Sale.objects.all():
                for q in s.Product_Quantity.all():
                    if q.product == p:
                        products_sale[p.name] += q.quantity
    except:
        products_sale = {}

    chart['series'] = [{
        'data': [],
        'name': 'Estadistica de mayores ventas',
        'type': 'pie',
        'radius': '50%',
        'emphasis': {
            'itemStyle': {
                'shadowBlur': 10,
                'shadowOffsetX': 0,
                'shadowColor': 'rgba(0, 0, 0, 0.5)'
            }
        }
    }]
    # Lista de productos con su nombre
    names = list(products_sale.keys())
    quantity = list(products_sale.values())

    for i in range(len(names)):
        if quantity[i] > 0:
            chart['series'][0]['data'].append({
                'value': quantity[i],
                'name': names[i]
            })

    # Ordenar de mayor a menor
    products_sale = dict(sorted(products_sale.items(), key=lambda item: item[1], reverse=True))
    return JsonResponse(chart)

def get_favorite(request):
    chart = {
        'tooltip': {
            'trigger': 'item',
        },
        'legend': {
            'orient': 'vertical',
            'left': 'left',
        },
    }
    try:
        products = Product.objects.all()
        products_favorite = {}
        for p in products:
            products_favorite[p.name] = 0
            for f in Favorite.objects.all():
                if f.product == p:
                    products_favorite[p.name] += 1
    except:
        products_favorite = {}

    chart['series'] = [{
        'data': [],
        'name': 'Estadistica de favoritos',
        'type': 'pie',
        'radius': '50%',
        'emphasis': {
            'itemStyle': {
                'shadowBlur': 10,
                'shadowOffsetX': 0,
                'shadowColor': 'rgba(0, 0, 0, 0.5)'
            }
        }
    }]
    # Lista de productos con su nombre
    names = list(products_favorite.keys())
    quantity = list(products_favorite.values())

    for i in range(len(names)):
        if quantity[i] > 0:
            chart['series'][0]['data'].append({
                'value': quantity[i],
                'name': names[i]
            })

    # Ordenar de mayor a menor
    products_favorite = dict(sorted(products_favorite.items(), key=lambda item: item[1], reverse=True))
    return JsonResponse(chart)

def get_sellers(request):
    chart = {
        'tooltip': {
            'trigger': 'item',
        },
        'legend': {
            'orient': 'vertical',
            'left': 'left',
        },
    }
    try:
        sellers = Seller.objects.all()
        sellers_sale = {}
        for s in sellers:
            sellers_sale[s.user.username] = 0
            for r in ClientSellerRelation.objects.all():
                if r.seller == s:
                    sellers_sale[s.user.username] += 1
    except:
        sellers_sale = {}

    chart['series'] = [{
        'data': [],
        'name': 'Estadistica de ventas por empleado',
        'type': 'pie',
        'radius': '50%',
        'emphasis': {
            'itemStyle': {
                'shadowBlur': 10,
                'shadowOffsetX': 0,
                'shadowColor': 'rgba(0, 0, 0, 0.5)'
            }
        }
    }]
    # Lista de productos con su nombre
    names = list(sellers_sale.keys())
    quantity = list(sellers_sale.values())

    for i in range(len(names)):
        if quantity[i] > 0:
            chart['series'][0]['data'].append({
                'value': quantity[i],
                'name': names[i]
            })

    # Ordenar de mayor a menor
    sellers_sale = dict(sorted(sellers_sale.items(), key=lambda item: item[1], reverse=True))
    return JsonResponse(chart)

def get_products_cart(request):
    chart = {
        'tooltip': {
            'trigger': 'item',
        },
        'legend': {
            'orient': 'vertical',
            'left': 'left',
        },
    }
    try:
        products = Product.objects.all()
        products_cart = {}
        for p in products:
            products_cart[p.name] = 0
            for c in Cart.objects.all():
                if c.product == p:
                    products_cart[p.name] += c.quantity
    except:
        products_cart = {}

    chart['series'] = [{
        'data': [],
        'name': 'Estadistica de productos en carrito',
        'type': 'pie',
        'radius': '50%',
        'emphasis': {
            'itemStyle': {
                'shadowBlur': 10,
                'shadowOffsetX': 0,
                'shadowColor': 'rgba(0, 0, 0, 0.5)'
            }
        }
    }]
    # Lista de productos con su nombre
    names = list(products_cart.keys())
    quantity = list(products_cart.values())

    for i in range(len(names)):
        if quantity[i] > 0:
            chart['series'][0]['data'].append({
                'value': quantity[i],
                'name': names[i]
            })

    # Ordenar de mayor a menor
    products_cart = dict(sorted(products_cart.items(), key=lambda item: item[1], reverse=True))
    return JsonResponse(chart)