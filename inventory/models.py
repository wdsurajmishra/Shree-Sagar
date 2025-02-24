from django.db import models
from django.utils.text import slugify
import uuid
from .validators import validate_thumbnail_size
from colorfield.fields import ColorField
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill, ResizeToFit



class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    thumbnail = ProcessedImageField(upload_to='category_thumbnails/',
                                    processors=[ResizeToFit(600, 600)],
                                    format='WEBP',
                                    options={'quality': 95})
    seo_meta_title = models.CharField(max_length=70, blank=True, null=True)
    seo_meta_description = models.CharField(
        max_length=160, blank=True, null=True)
    seo_meta_keywords = models.CharField(max_length=255, blank=True, null=True)
    additional_seo = models.TextField(
        blank=True, help_text="Additional SEO code or metadata")
    created_at = models.DateTimeField(auto_now_add=True)  # already present
    updated_at = models.DateTimeField(auto_now=True)  # already present

    class Meta:
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
        ]
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def products_count(self):
        products = Product.objects.filter(category=self).count()
        return products

    def __str__(self):
        return f"{self.name}"


class Subcategory(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    seo_meta_title = models.CharField(max_length=70, blank=True, null=True)
    seo_meta_description = models.CharField(
        max_length=160, blank=True, null=True)
    seo_meta_keywords = models.CharField(max_length=255, blank=True, null=True)
    additional_seo = models.TextField(
        blank=True, help_text="Additional SEO code or metadata")
    created_at = models.DateTimeField(auto_now_add=True)  # already present
    updated_at = models.DateTimeField(auto_now=True)  # already present

    class Meta:
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['category']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
        ]
        verbose_name = 'Subcategory'
        verbose_name_plural = 'Subcategories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"


class Size(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Size'
        verbose_name_plural = 'Sizes'


class Discount(models.Model):
    name = models.CharField(max_length=100)
    discount_type = models.CharField(
        max_length=10, choices=[('percentage', 'Percentage'), ('flat', 'Flat')])
    value = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    usage_limit = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)  # already present
    updated_at = models.DateTimeField(auto_now=True)  # already present

    class Meta:
        indexes = [
            models.Index(fields=['start_date']),
            models.Index(fields=['end_date']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
        ]
        verbose_name = 'Discount'
        verbose_name_plural = 'Discounts'

    def __str__(self):
        return f"{self.name} ({self.code})"

    def is_valid(self):
        """Check if the discount is currently valid based on date and active status."""
        now = timezone.now()
        return self.is_active and self.start_date <= now <= self.end_date


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    sku = models.CharField(max_length=100, unique=True, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='products')
    
    subcategory = models.ForeignKey(
        Subcategory, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    seller_pdf = models.FileField(upload_to='seller_pdfs/', blank=True, null=True)
    thumbnail = ProcessedImageField(upload_to='category_thumbnails/',
                                    processors=[ResizeToFit(1000, 1000)],
                                    format='WEBP',
                                    options={'quality': 95})
    tax = models.FloatField(default=0)
    is_active = models.BooleanField(default=True)
    seo_meta_title = models.CharField(max_length=70, blank=True, null=True)
    seo_meta_description = models.CharField(
        max_length=160, blank=True, null=True)
    seo_meta_keywords = models.CharField(max_length=255, blank=True, null=True)
    additional_seo = models.TextField(
        blank=True, help_text="Additional SEO code or metadata")
    created_at = models.DateTimeField(auto_now_add=True)  # already present
    updated_at = models.DateTimeField(auto_now=True)  # already present

    class Meta:
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['sku']),
            models.Index(fields=['category']),
            models.Index(fields=['subcategory']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
        ]
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.sku:
            self.sku = self.generate_sku()
        super().save(*args, **kwargs)

    def generate_sku(self):
        return f"SKU-{uuid.uuid4().hex[:8].upper()}"

    def __str__(self):
        return f"{self.name}"
    
    @staticmethod
    def generate_stock_report():
        """Generate a stock report for all products and their variants."""
        report = []
        products = Product.objects.all()
        for product in products:
            product_data = {
                'product_name': product.name,
                'variants': []
            }
            for variant in product.variants.all():
                variant_data = {
                    'variant_name': variant.name,
                    'variant_stock': variant.stock_quantity
                }
                product_data['variants'].append(variant_data)
            report.append(product_data)
        return report


class Color(models.Model):
    id = models.AutoField(primary_key=True)
    color = ColorField(default='#FFFFFF')
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class ProductVariant(models.Model):
    id = models.AutoField(primary_key=True)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='variants')
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['product']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
        ]
        verbose_name = 'Product Variant'
        verbose_name_plural = 'Product Variants'

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.product.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.color.name}"

    def get_discounted_price(self):
        """Calculate the product's price after applying any valid discount."""
        if self.discount and self.discount.is_valid():
            if self.discount.discount_type == 'percentage':
                discount_amount = (self.price * self.discount.value) / 100
                # Ensure price isn't negative
                return max(self.price - discount_amount, 0)
            elif self.discount.discount_type == 'flat':
                return max(self.price - self.discount.value, 0)
        return self.price  # Return original price if no valid discount

    def has_active_discount(self):
        """Check if the product has an active discount."""
        return self.discount and self.discount.is_valid()
    

    def get_thumbnail(self):
        thumb = ProductImage.objects.filter(product_variant=self).first()
        return thumb.image.url



class ProductReview(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    is_verified = models.BooleanField(default=False)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # already present
    updated_at = models.DateTimeField(auto_now=True)  # already present

    class Meta:
        indexes = [
            models.Index(fields=['product']),
            models.Index(fields=['user']),
            models.Index(fields=['rating']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
        ]
        verbose_name = 'Product Review'
        verbose_name_plural = 'Product Reviews'

    def __str__(self):
        return f"Review for {self.product.name} by {self.user.username}"


class ProductShipping(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='shipping_details')
    shipping_method = models.CharField(max_length=100)
    local_shipping_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    regional_shipping_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    national_shipping_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    shipping_cost_multiply_quantity = models.BooleanField(default=False)
    estimated_delivery_time = models.CharField(
        max_length=100, blank=True, null=True)
    additional_shipping_info = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # already present
    updated_at = models.DateTimeField(auto_now=True)  # already present

    class Meta:
        indexes = [
            models.Index(fields=['product']),
            models.Index(fields=['shipping_method']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
        ]
        verbose_name = 'Product Shipping'
        verbose_name_plural = 'Product Shippings'

    def __str__(self):
        return f"Shipping details for {self.product.name} - {self.shipping_method}"


class ProductImage(models.Model):
    product_variant = models.ForeignKey(
        ProductVariant, on_delete=models.CASCADE, related_name='images')
    image = ProcessedImageField(upload_to='product_images/',
                                    processors=[ResizeToFit(1500, 1500)],
                                    format='WEBP',
                                    options={'quality': 95})
    is_main = models.BooleanField(
        default=False, help_text="Indicates if this is the main image for the product.")
    created_at = models.DateTimeField(auto_now_add=True)  # already present
    updated_at = models.DateTimeField(auto_now=True)  # already present

    class Meta:
        indexes = [
            models.Index(fields=['product_variant']),
            models.Index(fields=['is_main']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
        ]
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'

    def __str__(self):
        return f"Image for {self.product_variant.color.name} - {'Main' if self.is_main else 'Secondary'}"


class ReviewImage(models.Model):
    review = models.ForeignKey(
        ProductReview, on_delete=models.CASCADE, related_name='images')
    image = ProcessedImageField(upload_to='category_thumbnails/',
                                    processors=[ResizeToFit(1500, 1500)],
                                    format='WEBP',
                                    options={'quality': 95})
    uploaded_at = models.DateTimeField(auto_now_add=True)  # already present

    class Meta:
        indexes = [
            models.Index(fields=['review']),
            models.Index(fields=['uploaded_at']),
        ]
        verbose_name = 'Review Image'
        verbose_name_plural = 'Review Images'

    def __str__(self):
        return f"Image for review of {self.review.product.name}"


class DiscountHistory(models.Model):
    discount = models.ForeignKey(
        Discount, on_delete=models.CASCADE, related_name='history')
    usage_count = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)  # already present

    class Meta:
        indexes = [
            models.Index(fields=['discount']),
            models.Index(fields=['timestamp']),
        ]
        verbose_name = 'Discount History'
        verbose_name_plural = 'Discount Histories'

    def __str__(self):
        return f"{self.discount.name} used {self.usage_count} times"


class PriceHistory(models.Model):
    product_variant = models.ForeignKey(
        ProductVariant, on_delete=models.CASCADE, related_name='price_history')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(
        auto_now_add=True, editable=False)  # already present

    class Meta:
        indexes = [
            models.Index(fields=['product_variant']),
            models.Index(fields=['timestamp']),
        ]
        verbose_name = 'Price History'
        verbose_name_plural = 'Price Histories'

    def __str__(self):
        return f"{self.product_variant.name} - Price: {self.price} on {self.timestamp}"


class InventoryTransaction(models.Model):
    product_variant = models.ForeignKey(
        ProductVariant, on_delete=models.CASCADE, related_name='inventory_transactions')
    quantity = models.IntegerField()
    transaction_type = models.CharField(
        max_length=10, choices=[('in', 'In'), ('out', 'Out')])
    created_at = models.DateTimeField(auto_now_add=True)  # already present

    class Meta:
        indexes = [
            models.Index(fields=['product_variant']),
            models.Index(fields=['created_at']),
        ]
        verbose_name = 'Inventory Transaction'
        verbose_name_plural = 'Inventory Transactions'

    def __str__(self):
        return f"{self.transaction_type.capitalize()} - {self.quantity} for {self.product_variant.name}"


class Coupon(models.Model):
    COUPON_SCOPE_CHOICES = [
        ('website', 'Full Website'),
        ('category', 'Selected Category'),
        ('product', 'Selected Product')
    ]

    code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(
        max_length=10, choices=[('percentage', 'Percentage'), ('flat', 'Flat')])
    value = models.DecimalField(max_digits=10, decimal_places=2)
    # Max times this coupon can be used across all users
    usage_limit = models.PositiveIntegerField(default=1)
    usage_count = models.PositiveIntegerField(
        default=0)  # Track current usage count
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True)
    scope = models.CharField(
        max_length=10, choices=COUPON_SCOPE_CHOICES, default='website')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code

    def clean(self):
        """Custom validation to ensure only valid combinations of scope, category, and product."""
        if self.scope == 'website':
            # For 'website' scope, category and product should both be null
            if self.category is not None or self.product is not None:
                raise ValidationError(
                    "For 'Full Website' coupon, category and product must be empty.")

        elif self.scope == 'category':
            # For 'category' scope, category should be set, and product should be null
            if self.category is None:
                raise ValidationError(
                    "For 'Selected Category' coupon, category must be selected.")
            if self.product is not None:
                raise ValidationError(
                    "For 'Selected Category' coupon, product must be empty.")

        elif self.scope == 'product':
            # For 'product' scope, product should be set, and category should be null
            if self.product is None:
                raise ValidationError(
                    "For 'Selected Product' coupon, product must be selected.")
            if self.category is not None:
                raise ValidationError(
                    "For 'Selected Product' coupon, category must be empty.")

    def is_valid(self):
        """Check if the coupon is valid based on usage limits and active status."""
        return self.is_active and self.usage_count < self.usage_limit

    def increment_usage(self):
        """Increase the usage count by one, if within limits."""
        if self.usage_count < self.usage_limit:
            self.usage_count += 1
            self.save()

    def apply_discount(self, item):
        """Apply the discount to a product or category based on the coupon scope."""
        if self.scope == 'website':
            # Apply to the entire website (all products)
            if self.discount_type == 'percentage':
                return item.price - (item.price * (self.value / 100))
            else:
                return item.price - self.value

        elif self.scope == 'category' and self.category == item.category:
            # Apply to items in a specific category
            if self.discount_type == 'percentage':
                return item.price - (item.price * (self.value / 100))
            else:
                return item.price - self.value

        elif self.scope == 'product' and self.product == item:
            # Apply to a specific product
            if self.discount_type == 'percentage':
                return item.price - (item.price * (self.value / 100))
            else:
                return item.price - self.value

        # Return original price if coupon doesn't apply
        return item.price


class CouponUsage(models.Model):
    coupon = models.ForeignKey(
        Coupon, on_delete=models.CASCADE, related_name='usages')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['coupon']),
            models.Index(fields=['user']),
            models.Index(fields=['created_at']),
        ]
        # Prevent multiple uses by the same user
        unique_together = ('coupon', 'user')

    def __str__(self):
        return f"Coupon: {self.coupon.code}, User: {self.user.username}"



class ProductFaq(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='faqs')
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"FAQ for {self.product.name} - {self.question[:20]}"
    

    class Meta:
        verbose_name = 'Product FAQ'
        verbose_name_plural = 'Product FAQs'