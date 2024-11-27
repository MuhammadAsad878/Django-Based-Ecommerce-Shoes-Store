from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from store.models import Product
from .cart import Cart


# View to display the cart summary
@csrf_exempt
def cart_summary(request):
    cart = Cart(request)
    cart_data = request.session.get('cart', {})
    cart_count = sum(item['quantity'] for item in cart_data.values())  # Calculate total items in cart
    cart_items = cart.cart.values()  # Get cart items as a list of dictionaries

    context = {
        'cart_items': cart_items,
        'cart_count': cart_count
    }
    return render(request, 'cart_summary.html', context)


# View to add a product to the cart
@csrf_exempt
def cart_add(request):
    if request.POST.get('action') == 'post':
        try:
            product_id = int(request.POST.get('product_id'))
            product = get_object_or_404(Product, id=product_id)
            cart = Cart(request)
            cart.add(product=product, productID=product_id)

            # Redirect to the homepage or another relevant page
            return redirect('/home')
        except (ValueError, Product.DoesNotExist):
            return HttpResponse("Invalid Product ID", status=400)
    return HttpResponse("Invalid Request", status=400)


# View to delete a product from the cart
@csrf_exempt
def cart_delete(request):
    if request.POST.get('action') == 'post':
        try:
            product_id = int(request.POST.get('product_id'))
            cart = Cart(request)
            cart.delete(product_id=product_id)

            # Redirect to the cart summary page
            return redirect('cart_summary')
        except (ValueError, KeyError, Exception) as e:
            return render(request, 'Error.html', {'data': f"Invalid Request: {e}"}, status=400)
    return HttpResponse("Invalid Request", status=400)


# View to update the quantity of a product in the cart
@csrf_exempt
def cart_update(request):
    if request.POST.get('action') == 'post':
        try:
            product_id = int(request.POST.get('product_id'))
            quantity = int(request.POST.get('quantity'))
            cart = Cart(request)
            cart.update(product_id=product_id, quantity=quantity)

            # Redirect to the cart summary page
            return redirect('cart_summary')
        except (ValueError, KeyError, Exception) as e:
            return HttpResponse(f"Error: {e}", status=400)
    return HttpResponse("Invalid Request", status=400)
