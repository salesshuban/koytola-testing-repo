# Generated by Django 3.1 on 2021-07-14 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_auto_20210712_1316'),
    ]

    operations = [
        migrations.AddField(
            model_name='portdeals',
            name='currency',
            field=models.CharField(default='USD', max_length=4),
        ),
    ]
