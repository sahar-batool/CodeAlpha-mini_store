from .models import Product

CART_SESSION_ID = "cart"


class Cart:
    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.setdefault(CART_SESSION_ID, {})

    def add(self, product, quantity=1, override=False):
        pid = str(product.id)
        current = self.cart.get(pid, 0)
        new_qty = quantity if override else current + quantity
        new_qty = min(new_qty, product.stock)  # can't exceed stock
        if new_qty <= 0:
            self.remove(product)
        else:
            self.cart[pid] = new_qty
            self.save()

    def remove(self, product):
        pid = str(product.id)
        if pid in self.cart:
            del self.cart[pid]
            self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        products = Product.objects.filter(id__in=self.cart.keys())
        for product in products:
            qty = self.cart[str(product.id)]
            yield {
                "product": product,
                "quantity": qty,
                "subtotal": product.price * qty,
            }

    def __len__(self):
        return sum(self.cart.values())

    def get_total(self):
        return sum(item["subtotal"] for item in self)

    def clear(self):
        self.session[CART_SESSION_ID] = {}
        self.save()