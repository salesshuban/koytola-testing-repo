# Generated by Django 3.1 on 2021-06-30 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='currency',
            field=models.CharField(max_length=4),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='currency',
            field=models.CharField(max_length=4),
        ),
    ]