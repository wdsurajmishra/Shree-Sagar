# Generated by Django 5.1.3 on 2025-01-07 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0010_color_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productvariant',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
