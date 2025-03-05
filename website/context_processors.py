from inventory.models import Category, Subcategory
from website.models import Home
from orders.models import ShippingAddress

def categories(request):
    categories_data = []
    for category in Category.objects.all().order_by('-id'):
        subcategories = Subcategory.objects.filter(category=category)
        if request.user.is_authenticated:
            addresses = ShippingAddress.objects.filter(customer=request.user)
        else:
            addresses = []

        categories_data.append({
            'category': category,
            'subcategories': subcategories,
        })

    return {
        'categories_data': categories_data,
        'addresses': addresses,
        'home': Home.objects.get(pk=1)
    }