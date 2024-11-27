from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from store.models import Product
from cart.cart import Cart


# Homepage view: Displays all products and cart count
@login_required(login_url='Index')
def HomePage(request):
    products = Product.objects.all()
    cart = request.session.get('cart', {})
    cart_count = sum(item['quantity'] for item in cart.values())
    context = {
        'products': products,
        'cart_count': cart_count
    }
    return render(request, 'home.html', context)


# Custom redirect for login-required pages
def custom_login_redirect(request):
    return render(request, 'Error.html', {'data': "Login First!"})


# Add a product to the cart
@csrf_exempt
@login_required(login_url='Index')
def add_to_cart(request):
    try:
        product_id = str(request.POST.get('product_id'))
        quantity = int(request.POST.get('quantity', 1))

        # Initialize or update the cart
        cart = request.session.get('cart', {})
        cart[product_id] = cart.get(product_id, 0) + quantity

        # Save cart to session
        request.session['cart'] = cart
        request.session.modified = True

        # Calculate cart count
        cart_count = sum(cart.values())
        return JsonResponse({'message': 'Product added to cart', 'cart_count': cart_count})
    except (ValueError, TypeError):
        return JsonResponse({'message': 'Invalid product ID or quantity'}, status=400)


# Get the total count of items in the cart
@login_required(login_url='Index')
def get_cart_count(request):
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())
    return JsonResponse({'cart_count': cart_count})


# View the cart: Displays cart items and total price
@login_required(login_url='Index')
def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            cart_items.append({'product': product, 'quantity': quantity})
            total_price += product.retail_price * quantity
        except Product.DoesNotExist:
            continue  # Skip if product doesn't exist

    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})


# Remove a product from the cart
@require_POST
@login_required(login_url='Index')
def remove_from_cart(request):
    product_id = request.POST.get('product_id')
    cart = request.session.get('cart', {})

    if product_id in cart:
        del cart[product_id]
        request.session['cart'] = cart
        request.session.modified = True

    return JsonResponse({'message': 'Product removed from cart', 'cart': cart})


# View a specific product's details
@login_required(login_url='Index')
def view_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    cart_count = sum(item['quantity'] for item in cart.values())
    return render(request, 'view_product.html', {'product': product, 'cart_count': cart_count})


# About Us page
@login_required(login_url='Index')
def AboutUs(request):
    cart = request.session.get('cart', {})
    cart_count = sum(item['quantity'] for item in cart.values())
    return render(request, 'aboutUs.html', {'cart_count': cart_count})


# Blog page
@login_required(login_url='Index')
def Blog(request):
    cart = request.session.get('cart', {})
    cart_count = sum(item['quantity'] for item in cart.values())
    return render(request, 'blog.html', {'cart_count': cart_count})


# Contact Us page
@login_required(login_url='Index')
def Contact(request):
    cart = request.session.get('cart', {})
    cart_count = sum(item['quantity'] for item in cart.values())
    return render(request, 'contactUs.html', {'cart_count': cart_count})
