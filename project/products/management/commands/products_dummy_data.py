from django.core.management.base import BaseCommand
from products.models import Brand, Category, Product
import random

class Command(BaseCommand):
    help = "Seed database with dummy data for categories, brands, and products."

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("Seeding dummy data..."))

        # ---------- Create Brands ----------
        brands = [
            "Apple", "Samsung", "Sony", "Dell", "HP", "Lenovo", "Asus", "LG", "Xiaomi", "Huawei"
        ]
        brand_objs = []
        for name in brands:
            brand, created = Brand.objects.get_or_create(name=name)
            brand_objs.append(brand)
        self.stdout.write(self.style.SUCCESS(f"✅ {len(brand_objs)} brands added."))

        # ---------- Create Categories ----------
        categories = [
            "Smartphones", "Laptops", "Monitors", "Headphones", "Smart Watches",
            "Gaming Accessories", "Printers", "Cameras", "TVs", "Networking Devices"
        ]
        category_objs = []
        for name in categories:
            category, created = Category.objects.get_or_create(name=name)
            category_objs.append(category)
        self.stdout.write(self.style.SUCCESS(f"✅ {len(category_objs)} categories added."))

        # ---------- Create Products ----------
        product_names = [
            "Pro Max", "Ultra HD", "Gaming Beast", "Smart Sound", "EliteBook",
            "ThinkPad", "IdeaPad", "Galaxy Watch", "PowerCam", "Noise Cancelling Pro"
        ]

        products = []
        for i in range(50):
            name = f"{random.choice(brands)} {random.choice(product_names)} {i+1}"
            product, created = Product.objects.get_or_create(
                name=name,
                defaults={
                    "factory": random.choice(brands),
                    "short_description": "High quality electronic product.",
                    "description": "This is a dummy product for testing the e-commerce API.",
                    "price": random.randint(1000, 20000),
                    "category": random.choice(category_objs),
                    "brand": random.choice(brand_objs),
                    "stock": random.randint(5, 100),
                    "code": f"SKU-{random.randint(10000, 99999)}",
                    "number_of_sales": random.randint(0, 500),
                    "rating": round(random.uniform(2.5, 5.0), 1),
                    "number_of_ratings": random.randint(1, 300),
                    "size": random.choice(["Small", "Medium", "Large"]),
                    "color": random.choice(["Black", "White", "Silver", "Gray", "Blue"]),
                    "weight": f"{random.randint(200, 3000)} g",
                    "additional_info": {"warranty": "1 year", "origin": "China"},
                }
            )
            products.append(product)

        self.stdout.write(self.style.SUCCESS(f"✅ {len(products)} products added."))

        self.stdout.write(self.style.SUCCESS("🎉 Seeding completed successfully!"))
