from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse, JsonResponse
from .cart import Cart
from store.models import Product
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def cart_summary(request):
    cart = Cart(request).cart  # Get the cart dictionary
    cart_items = cart.values()  # Get the cart items as a list of dictionaries
    return render(request, 'cart_summary.html', {'cart_items': cart_items})
@csrf_exempt
def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product = get_object_or_404(Product, id=product_id)
        print(product,product_id)
        cart.add(product=product,productID=product_id)
        response = {'message': f'Added {product.title} to cart.'}
        return JsonResponse(response)
    else:
        return HttpResponse("Invalid Request", status=400)
@csrf_exempt
def cart_delete(request):
    try:
      cart = Cart(request)
      if request.POST.get('action') == 'post':
          product_id = int(request.POST.get('product_id'))
          cart.delete(product_id=product_id)
          return redirect('cart_summary')
    except Exception as e:
        return render(request,'Error.html',{'data':f"Invalid Request{e} , status=400"})
@csrf_exempt
def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        print(request.POST.get('product_id'))
        product_id = int(request.POST.get('product_id'))
        quantity = int(request.POST.get('quantity'))
        cart.update(product_id=product_id, quantity=quantity)
        cart = Cart(request).cart  # Get the cart dictionary
        cart_items = cart.values()  # Get the cart items as a list of dictionaries
        return render(request, 'cart_summary.html', {'cart_items': cart_items})
    else:
        return HttpResponse("Invalid Request", status=400)
