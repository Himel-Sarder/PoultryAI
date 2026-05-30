from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Product, ProductImage, CATEGORY_CHOICES, Coupon
from .forms import ProductForm, ProductImageForm
from orders.models import Review


def product_list_view(request):
    products = Product.objects.filter(is_available=True).select_related('seller__farm_profile')
    category = request.GET.get('category', '')
    query = request.GET.get('q', '')
    if category:
        products = products.filter(category=category)
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(seller__farm_profile__farm_name__icontains=query)
        )
    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': CATEGORY_CHOICES,
        'selected_category': category,
        'query': query,
    })


def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk, is_available=True)
    reviews = Review.objects.filter(product=product).select_related('buyer')
    related_products = Product.objects.filter(
        category=product.category, is_available=True
    ).exclude(pk=pk)[:4]
    user_review = None
    if request.user.is_authenticated:
        user_review = reviews.filter(buyer=request.user).first()
    return render(request, 'products/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'related_products': related_products,
        'user_review': user_review,
    })


@login_required
def add_review_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST' and request.user.is_buyer:
        rating = int(request.POST.get('rating', 5))
        comment = request.POST.get('comment', '')
        review, created = Review.objects.update_or_create(
            product=product, buyer=request.user,
            defaults={'rating': rating, 'comment': comment}
        )
        messages.success(request, 'Review submitted successfully.')
    return redirect('products:product_detail', pk=pk)


@login_required
def seller_product_list_view(request):
    if not request.user.is_seller:
        return redirect('home')
    products = Product.objects.filter(seller=request.user)
    return render(request, 'products/seller_products.html', {'products': products})


@login_required
def add_product_view(request):
    if not request.user.is_seller:
        messages.error(request, 'Only sellers can add products.')
        return redirect('home')
    if not request.user.has_farm_profile:
        messages.error(request, 'Please complete your farm profile first.')
        return redirect('farms:create_farm')
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            images = request.FILES.getlist('images')
            for i, img in enumerate(images):
                ProductImage.objects.create(product=product, image=img, is_primary=(i == 0))
            messages.success(request, 'Product added successfully.')
            return redirect('products:seller_products')
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form, 'title': 'Add Product'})


@login_required
def edit_product_view(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            images = request.FILES.getlist('images')
            for i, img in enumerate(images):
                ProductImage.objects.create(product=product, image=img)
            messages.success(request, 'Product updated.')
            return redirect('products:seller_products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_form.html', {
        'form': form, 'product': product, 'title': 'Edit Product'
    })


@login_required
def delete_product_view(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted.')
    return redirect('products:seller_products')


@login_required
def delete_product_image_view(request, pk):
    img = get_object_or_404(ProductImage, pk=pk, product__seller=request.user)
    product_pk = img.product.pk
    img.delete()
    messages.success(request, 'Image deleted.')
    return redirect('products:edit_product', pk=product_pk)


def validate_coupon_view(request):
    import json
    from django.http import JsonResponse
    from django.utils import timezone
    if request.method == 'POST':
        code = request.POST.get('code', '').strip().upper()
        order_amount = float(request.POST.get('amount', 0))
        try:
            coupon = Coupon.objects.get(code=code)
            now = timezone.now()
            if not coupon.is_active:
                return JsonResponse({'valid': False, 'message': 'Coupon is inactive.'})
            if now < coupon.valid_from or now > coupon.valid_to:
                return JsonResponse({'valid': False, 'message': 'Coupon has expired.'})
            if coupon.used_count >= coupon.max_uses:
                return JsonResponse({'valid': False, 'message': 'Coupon usage limit reached.'})
            if order_amount < float(coupon.min_order_amount):
                return JsonResponse({'valid': False, 'message': f'Minimum order amount is ৳{coupon.min_order_amount}.'})
            discount = round(order_amount * coupon.discount_percent / 100, 2)
            return JsonResponse({
                'valid': True,
                'discount': discount,
                'percent': coupon.discount_percent,
                'message': f'{coupon.discount_percent}% discount applied!'
            })
        except Coupon.DoesNotExist:
            return JsonResponse({'valid': False, 'message': 'Invalid coupon code.'})
    return JsonResponse({'valid': False, 'message': 'Invalid request.'})
