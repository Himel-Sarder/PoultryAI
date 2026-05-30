from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction
from .models import Cart, CartItem, Order, OrderItem
from products.models import Product, Coupon
from notifications.models import Notification


@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(buyer=request.user)
    return render(request, 'orders/cart.html', {'cart': cart})


@login_required
def add_to_cart_view(request, product_id):
    if not request.user.is_buyer:
        messages.error(request, 'Only buyers can add to cart.')
        return redirect('products:product_detail', pk=product_id)
    product = get_object_or_404(Product, pk=product_id, is_available=True)
    cart, _ = Cart.objects.get_or_create(buyer=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        if cart_item.quantity < product.quantity:
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, f'Updated quantity for {product.name}.')
        else:
            messages.warning(request, 'Not enough stock available.')
    else:
        messages.success(request, f'{product.name} added to cart.')
    return redirect('orders:cart')


@login_required
def update_cart_view(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id, cart__buyer=request.user)
    action = request.POST.get('action')
    if action == 'increase':
        if item.quantity < item.product.quantity:
            item.quantity += 1
            item.save()
    elif action == 'decrease':
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()
    elif action == 'remove':
        item.delete()
    return redirect('orders:cart')


@login_required
def checkout_view(request):
    cart, _ = Cart.objects.get_or_create(buyer=request.user)
    if not cart.items.exists():
        messages.error(request, 'Your cart is empty.')
        return redirect('orders:cart')

    if request.method == 'POST':
        delivery_address = request.POST.get('delivery_address', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        payment_method = request.POST.get('payment_method', '')
        transaction_id = request.POST.get('transaction_id', '').strip()
        coupon_code = request.POST.get('coupon_code', '').strip().upper()

        if not all([delivery_address, phone_number, payment_method, transaction_id]):
            messages.error(request, 'All fields are required.')
            return render(request, 'orders/checkout.html', {'cart': cart})

        subtotal = cart.get_total()
        discount = 0
        valid_coupon = None

        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code)
                if coupon.is_valid() and subtotal >= coupon.min_order_amount:
                    discount = round(subtotal * coupon.discount_percent / 100, 2)
                    valid_coupon = coupon
                else:
                    messages.warning(request, 'Coupon is invalid or expired.')
            except Coupon.DoesNotExist:
                messages.warning(request, 'Invalid coupon code.')

        total = subtotal - discount

        # Group items by seller
        seller_items = {}
        for item in cart.items.all():
            seller = item.product.seller
            if seller not in seller_items:
                seller_items[seller] = []
            seller_items[seller].append(item)

        with transaction.atomic():
            orders_created = []
            for seller, items in seller_items.items():
                seller_subtotal = sum(i.get_subtotal() for i in items)
                seller_discount = round(discount * seller_subtotal / subtotal, 2) if subtotal > 0 else 0
                seller_total = seller_subtotal - seller_discount

                order = Order.objects.create(
                    buyer=request.user,
                    seller=seller,
                    delivery_address=delivery_address,
                    phone_number=phone_number,
                    payment_method=payment_method,
                    transaction_id=transaction_id,
                    coupon_code=coupon_code,
                    discount_amount=seller_discount,
                    subtotal=seller_subtotal,
                    total_amount=seller_total,
                )
                for item in items:
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        product_name=item.product.name,
                        product_price=item.product.price,
                        quantity=item.quantity,
                        subtotal=item.get_subtotal(),
                    )
                    # Reduce product quantity
                    item.product.quantity -= item.quantity
                    item.product.save()
                orders_created.append(order)

                # Notify seller
                Notification.objects.create(
                    user=seller,
                    title='New Order Received',
                    message=f'You have a new order #{order.pk} from {request.user.full_name}.',
                    notification_type='order',
                    link=f'/orders/seller/{order.pk}/'
                )

            if valid_coupon:
                valid_coupon.used_count += 1
                valid_coupon.save()

            cart.items.all().delete()

        # Notify buyer
        Notification.objects.create(
            user=request.user,
            title='Order Placed Successfully',
            message=f'Your order has been placed. Total: ৳{total}',
            notification_type='order',
            link='/orders/my-orders/'
        )

        messages.success(request, f'Order placed successfully! Total: ৳{total}')
        return redirect('orders:order_list')

    return render(request, 'orders/checkout.html', {'cart': cart})


@login_required
def order_list_view(request):
    if request.user.is_buyer:
        orders = Order.objects.filter(buyer=request.user)
    else:
        orders = Order.objects.filter(seller=request.user)
    status_filter = request.GET.get('status', '')
    if status_filter:
        orders = orders.filter(status=status_filter)
    return render(request, 'orders/order_list.html', {'orders': orders, 'status_filter': status_filter})


@login_required
def order_detail_view(request, pk):
    if request.user.is_buyer:
        order = get_object_or_404(Order, pk=pk, buyer=request.user)
    else:
        order = get_object_or_404(Order, pk=pk, seller=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
def seller_order_detail_view(request, pk):
    order = get_object_or_404(Order, pk=pk, seller=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
def cancel_order_view(request, pk):
    order = get_object_or_404(Order, pk=pk, buyer=request.user)
    if order.can_cancel():
        order.status = 'cancelled'
        order.save()
        # Restore product quantity
        for item in order.items.all():
            if item.product:
                item.product.quantity += item.quantity
                item.product.save()
        Notification.objects.create(
            user=order.seller,
            title='Order Cancelled',
            message=f'Order #{order.pk} has been cancelled by buyer.',
            notification_type='order',
            link=f'/orders/seller/{order.pk}/'
        )
        messages.success(request, 'Order cancelled.')
    else:
        messages.error(request, 'This order cannot be cancelled.')
    return redirect('orders:order_list')


@login_required
def update_order_status_view(request, pk):
    if not request.user.is_seller:
        messages.error(request, 'Access denied.')
        return redirect('home')
    order = get_object_or_404(Order, pk=pk, seller=request.user)
    new_status = request.POST.get('status')
    valid_statuses = ['processing', 'delivered', 'cancelled']
    if new_status in valid_statuses:
        order.status = new_status
        order.save()
        status_messages = {
            'processing': 'Order marked as processing.',
            'delivered': 'Order marked as delivered.',
            'cancelled': 'Order cancelled.',
        }
        Notification.objects.create(
            user=order.buyer,
            title='Order Status Updated',
            message=f'Your order #{order.pk} is now {new_status}.',
            notification_type='order',
            link='/orders/my-orders/'
        )
        messages.success(request, status_messages.get(new_status, 'Status updated.'))
    return redirect('orders:order_detail', pk=pk)
