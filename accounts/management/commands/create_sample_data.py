from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from accounts.models import User
from farms.models import FarmProfile
from products.models import Product, Coupon
from social.models import FarmPost


class Command(BaseCommand):
    help = 'Creates sample data for testing'

    def handle(self, *args, **kwargs):
        # Admin
        if not User.objects.filter(email='admin@poultry.com').exists():
            User.objects.create_superuser(
                email='admin@poultry.com',
                password='admin123',
                full_name='Admin User',
                phone_number='01700000000'
            )
            self.stdout.write(self.style.SUCCESS('Admin created: admin@poultry.com / admin123'))

        # Sellers
        seller_data = [
            ('Rahim Farmer', 'rahim@farm.com', '01711111111', 'Rahim Poultry Farm', 'Dhaka, Mirpur', 'We raise healthy desi murgi and collect fresh eggs daily.'),
            ('Karim Poultry', 'karim@farm.com', '01722222222', 'Karim Sonali Farm', 'Gazipur, Tongi', 'Specializing in Sonali and Broiler chicken with organic feed.'),
            ('Fatima Farms', 'fatima@farm.com', '01733333333', 'Fatima Desi Farm', 'Narayanganj, Siddhirganj', 'Pure desi murgi and country eggs from our family farm.'),
        ]

        sellers = []
        for full_name, email, phone, farm_name, location, desc in seller_data:
            if not User.objects.filter(email=email).exists():
                seller = User.objects.create_user(
                    email=email, password='seller123',
                    full_name=full_name, phone_number=phone, user_type='seller'
                )
                FarmProfile.objects.create(
                    seller=seller, farm_name=farm_name, location=location,
                    contact_number=phone, description=desc, is_verified=True
                )
                sellers.append(seller)
                self.stdout.write(self.style.SUCCESS(f'Seller created: {email} / seller123'))
            else:
                sellers.append(User.objects.get(email=email))

        # Buyer
        if not User.objects.filter(email='buyer@test.com').exists():
            User.objects.create_user(
                email='buyer@test.com', password='buyer123',
                full_name='Test Buyer', phone_number='01744444444', user_type='buyer'
            )
            self.stdout.write(self.style.SUCCESS('Buyer created: buyer@test.com / buyer123'))

        # Products
        products_data = [
            (sellers[0], 'Desi Murgi', 'desi_murgi', 450, 'kg', 30, 'Pure desi murgi raised on natural feed. No artificial hormones.', True),
            (sellers[0], 'Desi Egg (Hali)', 'egg', 80, 'hali', 100, 'Fresh country eggs collected daily. Rich in nutrients.', True),
            (sellers[1], 'Sonali Chicken', 'sonali', 280, 'kg', 50, 'Premium Sonali chicken, hybrid breed, tender and tasty.', True),
            (sellers[1], 'Broiler Chicken', 'broiler', 180, 'kg', 80, 'Farm-fresh broiler chicken, ready to cook.', True),
            (sellers[2], 'Desi Murgi (Live)', 'desi_murgi', 500, 'piece', 20, 'Live desi murgi for purchase. Healthy and active birds.', True),
            (sellers[2], 'Country Egg (Dozen)', 'egg', 130, 'dozen', 200, 'Organic country eggs, rich golden yolk, no chemicals.', True),
            (sellers[0], 'Duck (Haas)', 'duck', 380, 'piece', 15, 'Farm-raised ducks. Great for special occasions.', True),
            (sellers[1], 'Sonali Egg', 'egg', 90, 'hali', 80, 'Fresh Sonali chicken eggs, large size, nutritious.', True),
        ]

        for seller, name, category, price, unit, qty, desc, featured in products_data:
            if not Product.objects.filter(seller=seller, name=name).exists():
                Product.objects.create(
                    seller=seller, name=name, category=category,
                    price=price, unit=unit, quantity=qty,
                    description=desc, is_available=True, is_featured=featured
                )

        self.stdout.write(self.style.SUCCESS(f'{len(products_data)} products created'))

        # Coupon
        if not Coupon.objects.filter(code='WELCOME10').exists():
            Coupon.objects.create(
                code='WELCOME10', discount_percent=10,
                min_order_amount=200, max_uses=500,
                is_active=True,
                valid_from=timezone.now(),
                valid_to=timezone.now() + timedelta(days=365)
            )
            self.stdout.write(self.style.SUCCESS('Coupon created: WELCOME10 (10% off)'))

        # Sample Posts
        for seller in sellers:
            if not FarmPost.objects.filter(seller=seller).exists():
                FarmPost.objects.create(
                    seller=seller,
                    content=f'Welcome to {seller.farm_profile.farm_name}! We offer the freshest poultry products. Order now for quick delivery!'
                )

        self.stdout.write(self.style.SUCCESS('\n=== Sample Data Created Successfully ==='))
        self.stdout.write('Admin:  admin@poultry.com / admin123')
        self.stdout.write('Seller: rahim@farm.com / seller123')
        self.stdout.write('Buyer:  buyer@test.com / buyer123')
        self.stdout.write('Coupon: WELCOME10 (10% off)')
