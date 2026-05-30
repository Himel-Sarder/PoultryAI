from django.db import models
from accounts.models import User


CATEGORY_CHOICES = [
    ('desi_murgi', 'Desi Murgi'),
    ('egg', 'Egg'),
    ('sonali', 'Sonali Chicken'),
    ('broiler', 'Broiler Chicken'),
    ('duck', 'Duck'),
    ('turkey', 'Turkey'),
    ('other', 'Other'),
]

UNIT_CHOICES = [
    ('kg', 'Per KG'),
    ('piece', 'Per Piece'),
    ('mon', 'Per Mon'),
    ('dozen', 'Per Dozen'),
    ('hali', 'Per Hali'),
]


class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default='kg')
    quantity = models.PositiveIntegerField(default=0)
    description = models.TextField()
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.seller.full_name}"

    def get_primary_image(self):
        img = self.images.filter(is_primary=True).first()
        if not img:
            img = self.images.first()
        return img

    def get_avg_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return 0

    def get_review_count(self):
        return self.reviews.count()


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.product.name}"


class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount_percent = models.PositiveIntegerField()
    min_order_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    max_uses = models.PositiveIntegerField(default=100)
    used_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} - {self.discount_percent}% off"

    def is_valid(self):
        from django.utils import timezone
        now = timezone.now()
        return (self.is_active and self.valid_from <= now <= self.valid_to
                and self.used_count < self.max_uses)
