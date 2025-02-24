from import_export import resources
from .models import Product, ProductVariant

class ProductVariantResource(resources.ModelResource):
    
    class Meta:
        model = ProductVariant
        exclude = ('id', 'color', 'discount', 'is_active', 'created_at', 'updated_at')

        
        
    
    