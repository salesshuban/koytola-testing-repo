# Generated by Django 3.1 on 2021-09-02 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0005_contact_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificate',
            name='name',
            field=models.CharField(blank=True, max_length=128),
        ),
    ]
