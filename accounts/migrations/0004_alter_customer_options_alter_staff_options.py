# Generated by Django 5.1.3 on 2024-11-14 07:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_staff_role'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'verbose_name': 'Customer', 'verbose_name_plural': 'Customers'},
        ),
        migrations.AlterModelOptions(
            name='staff',
            options={'verbose_name': 'Staff', 'verbose_name_plural': 'Staffs'},
        ),
    ]
