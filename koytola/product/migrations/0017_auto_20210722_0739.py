# Generated by Django 3.1 on 2021-07-22 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0016_portdeals_is_expire'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(allow_unicode=True, max_length=255),
        ),
    ]
