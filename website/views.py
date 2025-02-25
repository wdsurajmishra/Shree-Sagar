from django.shortcuts import render,redirect
from inventory.models import *
from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .forms import CustomerForm, ShippingAddressForm, ContactForm
from accounts.models import Customer
from orders.models import ShippingAddress
from django.contrib.auth import login
from django.contrib import messages
from django.views.decorators.cache import cache_page
from .models import Slider, VideoCallBooking, Faq
from django.views.generic import CreateView
from django import forms
from datetime import datetime

# Create your views here.
# @cache_page(60 * 15)
def index(request):
    sliders = Slider.objects.all().order_by('position')
    context = {
            'sliders': sliders,
            'categories': Category.objects.all().order_by('-created_at'),
            'products':  Product.objects.prefetch_related(
                Prefetch(
                    'variants', queryset=ProductVariant.objects.select_related('discount')),
                Prefetch(
                    'reviews', queryset=ProductReview.objects.select_related('user'))
            ).select_related('category', 'subcategory'),
        }
    return render(request, 'website/pages/home.html', context)

# @cache_page(60 * 15)
def shop(request):
    category_id = request.GET.get('category')
    subcategory_id = request.GET.get('subcategory')
    color_id = request.GET.get('color')
    price_range = request.GET.get('price')

    products = Product.objects.prefetch_related(
        Prefetch(
            'variants', queryset=ProductVariant.objects.select_related('discount')),
        Prefetch(
            'reviews', queryset=ProductReview.objects.select_related('user'))
    ).select_related('category', 'subcategory')

    if category_id:
        products = products.filter(category_id=category_id)
    if subcategory_id:
        products = products.filter(subcategory_id=subcategory_id)
    if color_id:
        products = products.filter(variants__color_id=color_id)
    if price_range:
        min_price, max_price = map(int, price_range.split('-'))
        products = products.filter(variants__price__gte=min_price, variants__price__lte=max_price)

    context = {
        'categories': Category.objects.all().order_by('-created_at'),
        'subcategories': Subcategory.objects.all().order_by('-created_at'),
        'colors': Color.objects.all(),
        'products': products,
    }
    return render(request, 'website/pages/shop.html', context)

# @cache_page(60 * 15)
def product(request, slug):
    product = Product.objects.prefetch_related(
        Prefetch(
            'variants', queryset=ProductVariant.objects.select_related('discount')),
        Prefetch(
            'reviews', queryset=ProductReview.objects.select_related('user'))
    ).select_related('category', 'subcategory').get(slug=slug)
    
    related_products = Product.objects.prefetch_related(
        Prefetch(
            'variants', queryset=ProductVariant.objects.select_related('discount')),
        Prefetch(
            'reviews', queryset=ProductReview.objects.select_related('user'))
    ).select_related('category', 'subcategory').filter(category=product.category).exclude(id=product.id)[:4]

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'website/pages/product-detail.html', context)


# @cache_page(60 * 15)
def search(request):
    q = request.GET.get('q') or None

    if q:
        products = Product.objects.filter(name__icontains=q, description__icontains=q)
        return JsonResponse({'products': list(products.values('name', 'slug', 'price', 'thumbnail'))})
    
    return JsonResponse({'products': []})


def categories(request):
    categories = Category.objects.all().order_by('-created_at')
    return render(request, 'website/pages/categories.html', {'categories': categories})


@csrf_exempt
@require_POST
def add_to_cart(request):
    product_id = request.POST.get('product_id')
    product = get_object_or_404(ProductVariant, id=product_id)
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += 1
    else:
        cart[str(product_id)] = {
            'id': product.id,
            'quantity': 1,        }
    request.session['cart'] = cart
    return JsonResponse({'status': 'success', 'message': 'Product added to cart'})

@csrf_exempt
@require_POST
def update_cart(request):
    product_id = request.POST.get('product_id')
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart[str(product_id)]['quantity'] = quantity
            request.session['cart'] = cart
            return JsonResponse({'status': 'success', 'message': 'Cart updated'})
        else:
            del cart[str(product_id)]
            request.session['cart'] = cart
            return JsonResponse({'status': 'success', 'message': 'Product removed from cart'})
    return JsonResponse({'status': 'error', 'message': 'Product removed from cart'})

@csrf_exempt
@require_POST
def delete_from_cart(request):
    product_id = request.POST.get('product_id')
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
        return JsonResponse({'status': 'success', 'message': 'Product removed from cart'})
    return JsonResponse({'status': 'error', 'message': 'Product removed from cart'})

def get_cart(request):
    cart = request.session.get('cart', {})
    products = []
    total = 0
    for product_id, item in cart.items():
        product = ProductVariant.objects.select_related('product').get(id=product_id)
        total += product.price * item['quantity']
        products.append({
            'id': product.id,
            'name': product.product.name,
            'price': product.price,
            'quantity': item['quantity'],
            'thumbnail': product.get_thumbnail(),
        })
    return JsonResponse({'products': products, 'total': total})


@login_required
def userProfile(request):
    customer = get_object_or_404(Customer, username=request.user)
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('user-profile')
    return render(request, 'website/pages/user/profile.html', {'form': form})

@login_required
def userAddresses(request):
    customer = get_object_or_404(Customer, username=request.user)
    addresses = ShippingAddress.objects.filter(customer=customer)
    form  = ShippingAddressForm(initial={'customer': customer})
    if request.GET.get('update'):
        address = get_object_or_404(ShippingAddress, id=request.GET.get('update'))
        form = ShippingAddressForm(instance=address)
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.customer = customer
            address.save()
            messages.success(request, 'Address added successfully')
            return redirect('user-addresses')
    return render(request, 'website/pages/user/addresses.html', {'customer': customer, 'addresses': addresses, 'form': form})


@login_required
def updateAddress(request, address_id):
    customer = get_object_or_404(Customer, username=request.user)
    address = get_object_or_404(ShippingAddress, id=address_id, customer=customer)
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, 'Address updated successfully')
            return redirect('user-addresses')
    else:
        form = ShippingAddressForm(instance=address)
    return render(request, 'website/pages/user/update_address.html', {'form': form})

@login_required
def deleteAddress(request, address_id):
    customer = get_object_or_404(Customer, username=request.user)
    address = get_object_or_404(ShippingAddress, id=address_id, customer=customer)
    address.delete()
    messages.success(request, 'Address deleted successfully')
    return redirect('user-addresses')


def support(request):
    return render(request, 'website/pages/support.html')



def videoCallBooking(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == "POST":
        name = request.POST.get('name')
        date_str = request.POST.get('date')
        slot = request.POST.get('slot')

        if not name or not date_str or not slot:
            messages.error(request, 'All fields are required')
            return render(request, 'website/pages/video-call.html', {'product': product})

        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, 'Invalid date format. Use YYYY-MM-DD')
            return render(request, 'website/pages/video-call.html', {'product': product})

        if VideoCallBooking.objects.filter(date=date, slot=slot).exists():
            messages.error(request, 'This slot is already booked')
            return render(request, 'website/pages/video-call.html', {'product': product})

        VideoCallBooking.objects.create(name=name, date=date, slot=slot, product=product)
        messages.success(request, 'Booking successful')
        whatsapp_url = f"https://wa.me/?text=Booking%20successful%20for%20{product.name}%20on%20{date_str}%20at%20{slot}"
        return redirect(whatsapp_url, target='_blank')

    return render(request, 'website/pages/video-call.html', {'product': product})


def available_slots(request):
    date_str = request.GET.get('date')
    if not date_str:
        return JsonResponse({'status': 'error', 'message': 'Date parameter is required'}, status=400)
    
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'status': 'error', 'message': 'Invalid date format. Use YYYY-MM-DD'}, status=400)
    
    booked_slots = VideoCallBooking.objects.filter(date=date).values_list('slot', flat=True)
    available_slots = [slot for slot, _ in VideoCallBooking.SLOT_CHOICES if slot not in booked_slots]
    
    return JsonResponse({'status': 'success', 'available_slots': available_slots})


def faq(request):
    faqs = Faq.objects.all().order_by('position')
    context = {"faqs": faqs}
    return render(request, 'website/pages/faq.html', context)

def our_story(request):
    return render(request, 'website/pages/our-story.html')

def history(request):
    return render(request, 'website/pages/history.html')

def contact(request):
    form = ContactForm()
    context = {'form': form}
    return render(request, 'website/pages/contact.html', context)    


def bestseller(request):
    products = Product.objects.prefetch_related(
        Prefetch(
            'variants', queryset=ProductVariant.objects.select_related('discount')),
        Prefetch(
            'reviews', queryset=ProductReview.objects.select_related('user'))
    ).select_related('category', 'subcategory').order_by('-created_at')[:12]
    context = {
        'products': products,
    }
    return render(request, 'website/pages/bestseller.html', context)