from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit, ResizeToFill
from django.utils import timezone
from datetime import timedelta
# Create your models here.
from django.contrib.auth.models import Group, User
from inventory.models import Product
from PIL import Image, ExifTags
from io import BytesIO
from django.core.files.base import ContentFile

from django.contrib.auth.hashers import make_password


def correct_image_orientation(image_field, original_name):
    image = Image.open(image_field)
    
    try:
        # Get the EXIF data
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break

        exif = image._getexif()
        if exif is not None:
            orientation = exif.get(orientation, None)

            # Rotate image based on orientation
            if orientation == 3:
                image = image.rotate(180, expand=True)
            elif orientation == 6:
                image = image.rotate(270, expand=True)
            elif orientation == 8:
                image = image.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        # If no EXIF data, continue without changes
        pass

    # Save the corrected image back to the field
    buffer = BytesIO()
    image.save(buffer, format="WEBP", quality=100)
    buffer.seek(0)

    # Pass the original file name or create a new one
    new_name = f"corrected_{original_name.split('.')[0]}.webp"
    return ContentFile(buffer.getvalue(), name=new_name)



class Roles(Group):
    class Meta:
        proxy = True
        verbose_name = verbose_name_plural = 'Roles'


class Staff(User):
    role = models.ForeignKey(Roles, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, unique=True)
    profile_picture = ProcessedImageField(
        upload_to='profile_pictures',
        processors=[ResizeToFill(500, 500)],
        format='WEBP',
        options={'quality': 100},
        blank=True,
        null=True
    )
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'staff_user'
        verbose_name  = 'Staff'
        verbose_name_plural = 'Staffs'

    def save(self, *args, **kwargs):
        self.is_staff = True
        self.save()
        super().save(*args, **kwargs) 


    def generate_otp(self):
        import random
        self.otp = str(random.randint(100000, 999999))
        self.otp_created_at = timezone.now()
        self.save()

    def is_otp_valid(self, otp):
        if self.otp == otp and self.otp_created_at + timedelta(minutes=10) > timezone.now():
            return True
        return False
           


class Customer(User):
    phone = models.CharField(max_length=15, unique=True)
    profile_picture = ProcessedImageField(
        upload_to='profile_pictures',
        processors=[ResizeToFill(500, 500)],
        format='WEBP',
        options={'quality': 100},
        blank=True,
        null=True
    )
    ban = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'customer_user'
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def generate_otp(self):
        import random

        self.otp = str(random.randint(100000, 999999))
        self.otp_created_at = timezone.now()
        self.save()

    def is_otp_valid(self, otp):
        if self.otp == otp and self.otp_created_at + timedelta(minutes=10) > timezone.now():
            return True
        return False
    
    def save(self, *args, **kwargs):
        if self.pk is None or not Customer.objects.filter(pk=self.pk, password=self.password).exists():
            self.password = make_password(self.password)
        if self.profile_picture:
            # Correct the orientation of the image
            self.profile_picture = correct_image_orientation(self.profile_picture, self.profile_picture.name)


        super().save(*args, **kwargs)
    

class Wallet(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'wallet'
        verbose_name = 'Wallet'
        verbose_name_plural = 'Wallets'

    def __str__(self):
        return f'{self.user.username}\'s Wallet'   
    

class WalletHistory(models.Model):
    id = models.AutoField(primary_key=True)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'wallet_history'
        verbose_name = 'Wallet History'
        verbose_name_plural = 'Wallet Histories'

    def __str__(self):
        return f'{self.wallet.user.username}\'s Wallet History'    
    

class WishList(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'wishlist'
        verbose_name = 'Wish List'
        verbose_name_plural = 'Wish Lists'

    def __str__(self):
        return f'{self.user.username}\'s Wish List'
    