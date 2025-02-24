# Generated by Django 5.1.3 on 2024-11-14 07:00

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0004_alter_customer_options_alter_staff_options'),
        ('inventory', '0005_product_is_active_productvariant_is_active'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255, verbose_name='Full Name')),
                ('address_line_1', models.CharField(max_length=255, verbose_name='Address Line 1')),
                ('address_line_2', models.CharField(blank=True, max_length=255, null=True, verbose_name='Address Line 2')),
                ('city', models.CharField(max_length=100, verbose_name='City')),
                ('state', models.CharField(max_length=100, verbose_name='State')),
                ('postal_code', models.CharField(max_length=20, verbose_name='Postal Code')),
                ('country', models.CharField(max_length=100, verbose_name='Country')),
                ('phone_number', models.CharField(max_length=20, verbose_name='Phone Number')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shipping_addresses', to='accounts.customer', verbose_name='Customer')),
            ],
            options={
                'verbose_name': 'Shipping Address',
                'verbose_name_plural': 'Shipping Addresses',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Order ID')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('processing', 'Processing'), ('shipped', 'Shipped'), ('delivered', 'Delivered'), ('cancelled', 'Cancelled')], default='pending', max_length=20, verbose_name='Status')),
                ('shipping_charge', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Shipping Charge')),
                ('discount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Discount')),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Total Amount')),
                ('tracking_id', models.CharField(blank=True, max_length=100, null=True, verbose_name='Tracking ID')),
                ('tracking_link', models.URLField(blank=True, null=True, verbose_name='Tracking Link')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='User')),
                ('shipping_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='orders.shippingaddress', verbose_name='Shipping Address')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Quantity')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Price')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.order', verbose_name='Order')),
                ('product_variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.productvariant', verbose_name='Product Variant')),
            ],
            options={
                'verbose_name': 'Order Item',
                'verbose_name_plural': 'Order Items',
                'indexes': [models.Index(fields=['order'], name='orders_orde_order_i_5d347b_idx'), models.Index(fields=['product_variant'], name='orders_orde_product_c4062e_idx')],
            },
        ),
        migrations.CreateModel(
            name='OrderStatusHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('processing', 'Processing'), ('shipped', 'Shipped'), ('delivered', 'Delivered'), ('cancelled', 'Cancelled')], max_length=20, verbose_name='Status')),
                ('changed_at', models.DateTimeField(auto_now_add=True, verbose_name='Changed At')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='status_history', to='orders.order', verbose_name='Order')),
            ],
            options={
                'verbose_name': 'Order Status History',
                'verbose_name_plural': 'Order Status Histories',
                'indexes': [models.Index(fields=['order'], name='orders_orde_order_i_f43086_idx'), models.Index(fields=['changed_at'], name='orders_orde_changed_14af81_idx')],
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method', models.CharField(choices=[('online', 'Online'), ('cash_on_delivery', 'Cash on Delivery')], max_length=20, verbose_name='Method')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Amount')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending', max_length=20, verbose_name='Status')),
                ('transaction_id', models.CharField(blank=True, max_length=100, null=True, verbose_name='Transaction ID')),
                ('payment_date', models.DateTimeField(auto_now_add=True, verbose_name='Payment Date')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='orders.order', verbose_name='Order')),
            ],
            options={
                'verbose_name': 'Payment',
                'verbose_name_plural': 'Payments',
                'indexes': [models.Index(fields=['order'], name='orders_paym_order_i_8c8d98_idx'), models.Index(fields=['status'], name='orders_paym_status_83f434_idx'), models.Index(fields=['payment_date'], name='orders_paym_payment_9e5ac0_idx')],
            },
        ),
        migrations.CreateModel(
            name='Refund',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Amount')),
                ('reason', models.TextField(verbose_name='Reason')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('processed', 'Processed')], default='pending', max_length=20, verbose_name='Status')),
                ('transaction_id', models.CharField(blank=True, max_length=100, null=True, verbose_name='Transaction ID')),
                ('refund_date', models.DateTimeField(auto_now_add=True, verbose_name='Refund Date')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='refunds', to='orders.order', verbose_name='Order')),
            ],
            options={
                'verbose_name': 'Refund',
                'verbose_name_plural': 'Refunds',
                'indexes': [models.Index(fields=['order'], name='orders_refu_order_i_341cd7_idx'), models.Index(fields=['status'], name='orders_refu_status_b87fcd_idx'), models.Index(fields=['refund_date'], name='orders_refu_refund__384984_idx'), models.Index(fields=['created_at'], name='orders_refu_created_8e3279_idx'), models.Index(fields=['updated_at'], name='orders_refu_updated_55c1f4_idx')],
            },
        ),
        migrations.AddIndex(
            model_name='shippingaddress',
            index=models.Index(fields=['customer'], name='orders_ship_custome_0842f9_idx'),
        ),
        migrations.AddIndex(
            model_name='shippingaddress',
            index=models.Index(fields=['city'], name='orders_ship_city_3b1494_idx'),
        ),
        migrations.AddIndex(
            model_name='shippingaddress',
            index=models.Index(fields=['state'], name='orders_ship_state_60efcc_idx'),
        ),
        migrations.AddIndex(
            model_name='shippingaddress',
            index=models.Index(fields=['postal_code'], name='orders_ship_postal__a6f271_idx'),
        ),
        migrations.AddIndex(
            model_name='shippingaddress',
            index=models.Index(fields=['country'], name='orders_ship_country_71c83c_idx'),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['order_id'], name='orders_orde_order_i_205064_idx'),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['status'], name='orders_orde_status_c6dd84_idx'),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['created_at'], name='orders_orde_created_0e92de_idx'),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['updated_at'], name='orders_orde_updated_94e16c_idx'),
        ),
    ]
