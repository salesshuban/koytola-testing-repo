# Generated by Django 3.1 on 2021-09-08 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0008_remove_contact_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='website',
            field=models.CharField(blank=True, default='', max_length=250),
        ),
    ]
