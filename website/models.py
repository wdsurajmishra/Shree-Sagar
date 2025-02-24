from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from inventory.models import Product
from tinymce.models import HTMLField

# Create your models here.
class Slider(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    position = models.PositiveIntegerField(unique=True)
    image = ProcessedImageField(
        upload_to='slider/',
        processors=[ResizeToFill(1800, 900)],
        format='JPEG',
        options={'quality': 90}
    )

    def __str__(self):
        return self.title
    
class Home(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    offer_text_with_link = models.TextField(blank=True, null=True, help_text="Offer text with link in html format")
    manufacturer_text = models.TextField(blank=True, null=True, help_text="Manufacturer text in html format use <span> tag for highlighting")
    manufacturer_video = models.FileField(upload_to='home/', blank=True, null=True, help_text="Manufacturer video")
    deals_banner_1 = ProcessedImageField(
        upload_to='home/',
        processors=[ResizeToFill(722, 420)],
        format='WEBP',
        options={'quality': 90},
        blank=True,
        null=True,
        help_text="Deals banner 1"
    )
    deals_banner_2 = ProcessedImageField(
        upload_to='home/',
        processors=[ResizeToFill(722, 420)],
        format='WEBP',
        options={'quality': 90},
        blank=True,
        null=True,
        help_text="Deals banner 2"
    )
    deals_banner_1_link = models.URLField(blank=True, null=True, help_text="Deals banner 1 link")
    deals_banner_2_link = models.URLField(blank=True, null=True, help_text="Deals banner 2 link")
    retail_background = ProcessedImageField(upload_to='home/', processors=[ResizeToFill(1440, 450)], format='WEBP', options={'quality': 90}, blank=True, null=True, help_text="Retail background")
    retail_text = models.TextField(blank=True, null=True, help_text="Retail text in html format")
    retail_link = models.URLField(blank=True, null=True, help_text="Retail link")
    seo_meta_title = models.CharField(max_length=70, blank=True, null=True)
    seo_meta_description = models.CharField(
        max_length=160, blank=True, null=True)
    seo_meta_keywords = models.CharField(max_length=255, blank=True, null=True)
    additional_seo = models.TextField(
        blank=True, help_text="Additional SEO code or metadata")
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Home Page"


class VideoCallBooking(models.Model):
    SLOT_CHOICES = [
        ('09:00-09:30', '09:00 AM - 09:30 AM'),
        ('09:30-10:00', '09:30 AM - 10:00 AM'),
        ('10:00-10:30', '10:00 AM - 10:30 AM'),
        ('10:30-11:00', '10:30 AM - 11:00 AM'),
        ('11:00-11:30', '11:00 AM - 11:30 AM'),
        ('11:30-12:00', '11:30 AM - 12:00 PM'),
        ('12:00-12:30', '12:00 PM - 12:30 PM'),
        ('12:30-13:00', '12:30 PM - 01:00 PM'),
        ('13:00-13:30', '01:00 PM - 01:30 PM'),
        ('13:30-14:00', '01:30 PM - 02:00 PM'),
        ('14:00-14:30', '02:00 PM - 02:30 PM'),
        ('14:30-15:00', '02:30 PM - 03:00 PM'),
        ('15:00-15:30', '03:00 PM - 03:30 PM'),
        ('15:30-16:00', '03:30 PM - 04:00 PM'),
        ('16:00-16:30', '04:00 PM - 04:30 PM'),
        ('16:30-17:00', '04:30 PM - 05:00 PM'),
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    date = models.DateField()
    slot = models.CharField(max_length=11, choices=SLOT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        unique_together = ['date', 'slot']
        verbose_name_plural = "Video Call Booking"

class Faq(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.CharField(max_length=255)
    answer = HTMLField()
    position = models.PositiveIntegerField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question