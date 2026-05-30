from .models import Cart


def cart_count(request):
    count = 0
    if request.user.is_authenticated and request.user.is_buyer:
        try:
            cart = Cart.objects.get(buyer=request.user)
            count = cart.get_item_count()
        except Cart.DoesNotExist:
            pass
    return {'cart_count': count}
