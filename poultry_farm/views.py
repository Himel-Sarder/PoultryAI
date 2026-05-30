from django.shortcuts import render
from products.models import Product, CATEGORY_CHOICES
from farms.models import FarmProfile


def home_view(request):
    featured_products = Product.objects.filter(is_available=True, is_featured=True).select_related('seller__farm_profile')[:8]
    if featured_products.count() < 4:
        featured_products = Product.objects.filter(is_available=True).select_related('seller__farm_profile')[:8]
    featured_farms = FarmProfile.objects.filter(is_verified=True)[:6]
    desi_products = Product.objects.filter(is_available=True, category='desi_murgi')[:4]
    egg_products = Product.objects.filter(is_available=True, category='egg')[:4]
    sonali_products = Product.objects.filter(is_available=True, category='sonali')[:4]
    return render(request, 'home.html', {
        'featured_products': featured_products,
        'featured_farms': featured_farms,
        'categories': CATEGORY_CHOICES,
        'desi_products': desi_products,
        'egg_products': egg_products,
        'sonali_products': sonali_products,
    })
