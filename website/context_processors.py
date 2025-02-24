from inventory.models import Category, Subcategory
from website.models import Home

def categories(request):
    categories_data = []
    for category in Category.objects.all().order_by('-id'):
        subcategories = Subcategory.objects.filter(category=category)
        categories_data.append({
            'category': category,
            'subcategories': subcategories
        })

    return {
        'categories_data': categories_data,
        'home': Home.objects.get(pk=1)
    }