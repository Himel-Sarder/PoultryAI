from django.db import models
from accounts.models import User


class FarmProfile(models.Model):
    seller = models.OneToOneField(User, on_delete=models.CASCADE, related_name='farm_profile')
    farm_name = models.CharField(max_length=200)
    location = models.CharField(max_length=300)
    farm_image = models.ImageField(upload_to='farms/', null=True, blank=True)
    contact_number = models.CharField(max_length=20)
    description = models.TextField()
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.farm_name

    def get_total_products(self):
        return self.seller.products.filter(is_available=True).count()

    def get_rating(self):
        from orders.models import Review
        reviews = Review.objects.filter(product__seller=self.seller)
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return 0
