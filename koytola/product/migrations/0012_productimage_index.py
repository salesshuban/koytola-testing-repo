# Generated by Django 3.1 on 2021-07-15 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0011_portdeals_quantity_unit'),
    ]

    operations = [
        migrations.AddField(
            model_name='productimage',
            name='index',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
