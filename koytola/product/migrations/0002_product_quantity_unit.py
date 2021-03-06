# Generated by Django 3.1 on 2021-06-25 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='quantity_unit',
            field=models.CharField(blank='item', choices=[('centimeter', 'Centi-Meter unit'), ('centimeter-square', 'Centi-Meter Square Unit'), ('centimeter-cube', 'Centi-Meter Cube Unit'), ('gallon', 'Gallon unit'), ('gram', 'Gram unit'), ('item', 'Item unit'), ('kilogram', 'Kilo-Gram unit'), ('lbm', 'Pound unit'), ('liter', 'Liter unit'), ('milligram', 'Milli-Gram unit'), ('millimeter', 'Milli-Meter unit'), ('millimeter-square', 'Milli-Meter Square unit'), ('millimeter-cube', 'Milli-Meter Cube unit'), ('meter', 'Meter unit'), ('meter-square', 'Meter Square Unit'), ('meter-cube', 'Meter Cube unit'), ('ounce', 'Ounce unit'), ('ton', 'Ton unit')], max_length=32, null=True),
        ),
    ]
