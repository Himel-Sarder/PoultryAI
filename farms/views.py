from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import FarmProfile
from .forms import FarmProfileForm
from products.models import Product
from social.models import FarmPost


def farm_list_view(request):
    query = request.GET.get('q', '')
    farms = FarmProfile.objects.filter(is_verified=True)
    if query:
        farms = farms.filter(
            Q(farm_name__icontains=query) |
            Q(location__icontains=query) |
            Q(description__icontains=query)
        )
    return render(request, 'farms/farm_list.html', {'farms': farms, 'query': query})


def farm_detail_view(request, pk):
    farm = get_object_or_404(FarmProfile, pk=pk)
    products = Product.objects.filter(seller=farm.seller, is_available=True)
    posts = FarmPost.objects.filter(seller=farm.seller).order_by('-created_at')[:10]
    category = request.GET.get('category', '')
    if category:
        products = products.filter(category=category)
    return render(request, 'farms/farm_detail.html', {
        'farm': farm, 'products': products, 'posts': posts, 'selected_category': category
    })


@login_required
def create_farm_view(request):
    if not request.user.is_seller:
        messages.error(request, 'Only sellers can create farm profiles.')
        return redirect('home')
    if request.user.has_farm_profile:
        return redirect('farms:edit_farm')
    if request.method == 'POST':
        form = FarmProfileForm(request.POST, request.FILES)
        if form.is_valid():
            farm = form.save(commit=False)
            farm.seller = request.user
            farm.save()
            messages.success(request, 'Farm profile created! Pending admin verification.')
            return redirect('farms:my_farm')
    else:
        form = FarmProfileForm()
    return render(request, 'farms/farm_form.html', {'form': form, 'title': 'Create Farm Profile'})


@login_required
def edit_farm_view(request):
    if not request.user.is_seller:
        return redirect('home')
    farm = get_object_or_404(FarmProfile, seller=request.user)
    if request.method == 'POST':
        form = FarmProfileForm(request.POST, request.FILES, instance=farm)
        if form.is_valid():
            form.save()
            messages.success(request, 'Farm profile updated.')
            return redirect('farms:my_farm')
    else:
        form = FarmProfileForm(instance=farm)
    return render(request, 'farms/farm_form.html', {'form': form, 'title': 'Edit Farm Profile'})


@login_required
def my_farm_view(request):
    if not request.user.is_seller:
        return redirect('home')
    if not request.user.has_farm_profile:
        return redirect('farms:create_farm')
    farm = request.user.farm_profile
    products = Product.objects.filter(seller=request.user)
    return render(request, 'farms/my_farm.html', {'farm': farm, 'products': products})
