from .cart import Cart
from .models import Category


def cart(request):
    return {
        "cart": Cart(request),
        "footer_categories": Category.objects.all()[:6],
    }