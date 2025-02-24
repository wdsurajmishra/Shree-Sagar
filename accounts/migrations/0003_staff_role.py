# Generated by Django 5.1.3 on 2024-11-13 11:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_customer_otp_customer_otp_created_at_staff_otp_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='role',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='accounts.roles'),
            preserve_default=False,
        ),
    ]
