# Generated by Django 3.1 on 2021-07-12 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_auto_20210712_0647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portdeals',
            name='lat',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='portdeals',
            name='lng',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
