import random
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from store.models import Category, Product


CATALOG = {
    "Watches": [
        ("Chronograph", 120,
         "A precision watch with a built-in stopwatch and a sharp, sporty dial. Good for timing anything from workouts to cooking.",
         "https://images.unsplash.com/photo-1682179259680-1ad7fe8f6b95?q=80&w=585&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D"),
        ("Digital Watch", 45,
         "A lightweight watch with a clear digital display, backlight and alarm. Simple to read at a glance, day or night.",
         "https://images.unsplash.com/photo-1660844817855-3ecc7ef21f12?q=80&w=486&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D"),
        ("Minimal Watch", 85,
         "A slim, clean-faced watch with no clutter. Pairs easily with both casual and formal outfits.",
         "https://images.unsplash.com/photo-1637719752114-42a31081896c?q=80&w=954&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D"),
        ("Classic Watch", 99,
         "A timeless analog watch with a polished look. A reliable everyday choice for work or special occasions.",
         "https://images.unsplash.com/photo-1587836374828-4dbafa94cf0e?q=80&w=870&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D"),
    ],
    "Bags": [
        ("Backpack", 60,
         "A comfortable everyday backpack with room for books, a laptop and lunch. Padded straps make long days easier.",
         "https://images.unsplash.com/photo-1680039211156-66c721b87625?q=80&w=390&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D"),
        ("Tote Bag", 35,
         "A spacious, open-top tote for shopping, work or the beach. Light, simple and easy to grab.",
         "https://images.unsplash.com/photo-1578237493287-8d4d2b03591a?q=80&w=326&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D"),
        ("Messenger Bag", 55,
         "A cross-body bag with plenty of pockets for daily carry. Keeps your hands free on the move.",
         "https://images.unsplash.com/photo-1510783891783-80cda42ebfd2?q=80&w=874&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D"),
        ("Laptop Sleeve", 25,
         "A padded sleeve that protects your laptop from scratches and bumps. Slim enough to slide into any bag.",
         "https://plus.unsplash.com/premium_photo-1723651240584-dd53816aa197?q=80&w=886&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D"),
    ],
    "Shoes": [
        ("Runner", 80,
         "A cushioned running shoe designed for comfort over distance. Light on the foot with a supportive sole.",
         "https://images.unsplash.com/photo-1543508282-6319a3e2621f?q=80&w=415&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D"),
        ("Canvas Sneaker", 50,
         "A casual, lightweight sneaker with a soft canvas upper. A simple go-to for everyday wear.",
         "https://plus.unsplash.com/premium_photo-1682125177822-63c27a3830ea?q=80&w=387&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D"),
        ("Leather Boot", 130,
         "A sturdy boot with a classic leather look. Made for cooler weather and rough days.",
         "https://images.unsplash.com/photo-1605732440685-d0654d81aa30?q=80&w=870&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D"),
        ("Sandal", 30,
         "An open, breathable sandal for warm days. Easy to slip on and comfortable for walking.",
         "https://plus.unsplash.com/premium_photo-1711051513016-72baa1035293?q=80&w=387&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D"),
    ],
    "Electronics": [
        ("Wireless Earbuds", 50,
         "Compact earbuds with clear sound and a charging case. Pair them with your phone in seconds.",
         "https://plus.unsplash.com/premium_photo-1679513691474-73102089c117?q=80&w=813&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D"),
        ("Power Bank", 30,
         "A pocket-sized portable charger that gives your phone several full charges on the go.",
         "https://images.unsplash.com/photo-1706275399494-fb26bbc5da63?q=80&w=580&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D"),
        ("Bluetooth Speaker", 55,
         "A portable speaker with strong sound and a battery that lasts all day. Great for trips and parties.",
         "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?q=80&w=1031&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D"),
        ("Phone Case", 15,
         "A slim protective case with raised edges to guard your screen and camera against drops.",
         "https://images.unsplash.com/photo-1623394088867-503931dff665?q=80&w=387&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D"),
    ],
    "Clothing": [
        ("Cotton T-Shirt", 20,
         "A soft, breathable cotton t-shirt with a relaxed fit. Easy to wear on its own or layered.",
         "https://images.unsplash.com/photo-1693443687750-611ad77f3aba?q=80&w=870&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D"),
        ("Hoodie", 45,
         "A warm fleece-lined hoodie with a front pocket and an adjustable hood. Made for cool evenings.",
         "https://images.unsplash.com/photo-1680292783974-a9a336c10366?q=80&w=394&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D"),
        ("Denim Jacket", 75,
         "A classic denim jacket that goes with almost everything. Sturdy, comfortable and long-lasting.",
         "https://plus.unsplash.com/premium_photo-1671030274122-b6ac34f87b8b?q=80&w=870&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D"),
        ("Baseball Cap", 18,
         "An adjustable cotton cap with a curved brim. Keeps the sun off and goes with any casual outfit.",
         "https://plus.unsplash.com/premium_photo-1680859126205-1c593bb4f9e8?q=80&w=387&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D"),
    ],
    "Accessories": [
        ("Sunglasses", 40,
         "Lightweight sunglasses with UV protection and a durable frame. Comfortable for all-day wear.",
         "https://images.unsplash.com/photo-1511499767150-a48a237f0083?q=80&w=580&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D"),
        ("Leather Wallet", 35,
         "A slim leather wallet with card slots and a bill compartment. Fits easily in a pocket.",
         "https://plus.unsplash.com/premium_photo-1681589453747-53fd893fa420?q=80&w=869&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D"),
        ("Leather Belt", 28,
         "A classic leather belt with a metal buckle. Works with both jeans and smarter trousers.",
         "https://images.unsplash.com/photo-1666723043169-22e29545675c?q=80&w=387&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D"),
        ("Wool Scarf", 32,
         "A soft wool scarf that keeps you warm in cold weather. Easy to style and easy to pack.",
         "https://plus.unsplash.com/premium_photo-1758742058691-b2bad88e987d?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D"),
    ],
}


class Command(BaseCommand):
    help = "Create sample categories (4 products each). Use --reset to clear old products first."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete existing products first (products that appear in orders are hidden instead)",
        )

    def handle(self, *args, **options):
        reset = options["reset"]

        if reset:
            deleted = hidden = 0
            for product in Product.objects.all():
                if product.orderitem_set.exists():
                    product.available = False
                    product.save(update_fields=["available"])
                    hidden += 1
                else:
                    product.delete()
                    deleted += 1
            Category.objects.filter(products__isnull=True).delete()
            self.stdout.write(f"Reset: {deleted} products deleted, {hidden} hidden (they have orders).")

        created = updated = 0

        for cat_name, items in CATALOG.items():
            category, _ = Category.objects.get_or_create(
                slug=slugify(cat_name), defaults={"name": cat_name}
            )

            for name, price, description, image_url in items:
                product, was_created = Product.objects.get_or_create(
                    slug=slugify(name),
                    defaults={
                        "category": category,
                        "name": name,
                        "description": description,
                        "price": Decimal(price),
                        "image_url": image_url,
                        "stock": random.randint(5, 25),
                    },
                )

                if was_created:
                    created += 1
                    continue

                # Existing product: only touch the image link (and unhide after --reset)
                changed = []
                if image_url and product.image_url != image_url:
                    product.image_url = image_url
                    changed.append("image_url")
                if reset and not product.available:
                    product.available = True
                    changed.append("available")
                if changed:
                    product.save(update_fields=changed)
                    updated += 1

        self.stdout.write(self.style.SUCCESS(
            f"Done. {created} products created, {updated} existing products updated."
        ))