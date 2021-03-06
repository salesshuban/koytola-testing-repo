# Generated by Django 3.1 on 2021-09-06 07:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0008_remove_contact_company'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0022_remove_productquery_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='productquery',
            name='seller',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='seller_query', to='profile.company'),
        ),
        migrations.AddField(
            model_name='productquery',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='buyer_query', to=settings.AUTH_USER_MODEL),
        ),
    ]
