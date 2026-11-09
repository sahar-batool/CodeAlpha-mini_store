from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .cart import Cart
from .forms import RegisterForm, OrderForm
from .models import Category, Product, Order, OrderItem
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth import views as auth_views
from .ratelimit import client_ip, is_limited, record_attempt




def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    query = request.GET.get("q", "").strip()
    if query:
        products = products.filter(name__icontains=query)

    paginator = Paginator(products, 12)
    page_obj = paginator.get_page(request.GET.get("page"))


    params = request.GET.copy()
    params.pop("page", None)

    return render(request, "store/product_list.html", {
        "category": category,
        "categories": categories,
        "page_obj": page_obj,
        "query": query,
        "querystring": params.urlencode(),
    })



def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    related = Product.objects.filter(
        category=product.category, available=True
    ).exclude(id=product.id)[:4]
    return render(request, "store/product_detail.html", {
        "product": product,
        "related": related,
    })


@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id, available=True)
    try:
        quantity = int(request.POST.get("quantity", 1))
    except ValueError:
        quantity = 1
    override = request.POST.get("override") == "1"

    cart = Cart(request)
    cart.add(product, quantity, override)

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({
            "cart_count": len(cart),
            "message": f"{product.name} added to cart",
        })
    return redirect("cart_detail")


@require_POST
def cart_remove(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Cart(request).remove(product)
    return redirect("cart_detail")


def cart_detail(request):
    return render(request, "store/cart.html", {"cart": Cart(request)})


def register(request):
    if request.user.is_authenticated:
        return redirect("product_list")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # log them in right after signing up
            return redirect("product_list")
    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {"form": form})



@login_required
def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect("cart_detail")

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    ids = [int(pid) for pid in cart.cart.keys()]
                    products = list(
                        Product.objects.select_for_update().filter(id__in=ids, available=True)
                    )
                    if len(products) != len(ids):
                        raise ValueError("Some items in your cart are no longer available.")

                    order = form.save(commit=False)
                    order.user = request.user
                    order.save()

                    for product in products:
                        qty = cart.cart[str(product.id)]
                        if qty > product.stock:
                            raise ValueError(f"Not enough stock for {product.name}.")
                        OrderItem.objects.create(
                            order=order, product=product, price=product.price, quantity=qty
                        )
                        product.stock -= qty
                        product.save(update_fields=["stock"])
            except ValueError as error:
                messages.error(request, str(error))
                return redirect("cart_detail")

            cart.clear()
            messages.success(request, f"Thank you! Your order #{order.id} has been placed.")
            return redirect("order_detail", order_id=order.id)
    else:
        form = OrderForm(initial={"email": request.user.email})

    return render(request, "store/checkout.html", {"cart": cart, "form": form})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "store/order_detail.html", {"order": order})


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).prefetch_related("items__product")
    return render(request, "store/order_list.html", {"orders": orders})


def _image(product):
    """Uploaded image if the model has one, otherwise the pasted link."""
    return getattr(product, "image_src", "") or product.image_url



def home(request):
    available = Product.objects.filter(available=True)

    new_arrivals = list(available[:8])
    budget = list(available.filter(price__lte=50).order_by("price")[:8])

   
    by_category = {}
    for p in available[:60]:
        img = _image(p)
        if img:
            p.hero_img = img
            by_category.setdefault(p.category_id, []).append(p)

    pool = []
    while len(pool) < 9 and any(by_category.values()):
        for items in by_category.values():
            if items and len(pool) < 9:
                pool.append(items.pop(0))

 
    hero_slots = [s for s in (pool[i::3] for i in range(3)) if s]

    categories = []
    for c in Category.objects.prefetch_related("products"):
        items = [p for p in c.products.all() if p.available]
        if not items:
            continue
        c.count = len(items)
        c.cover = next((_image(p) for p in items if _image(p)), "")
        categories.append(c)

    return render(request, "store/home.html", {
        "hero_slots": hero_slots,
        "categories": categories,
        "new_arrivals": new_arrivals,
        "budget": budget,
    })


class RateLimitedPasswordResetView(auth_views.PasswordResetView):
    def form_valid(self, form):
        email = form.cleaned_data["email"]
        ip = client_ip(self.request)
        if is_limited(email, ip):
            form.add_error("email", "Too many reset requests. Please wait a while and try again.")
            return self.form_invalid(form)
        record_attempt(email, ip)
        return super().form_valid(form)

