# Generated by Django 3.1 on 2021-09-02 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_user_linkedin_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='linkedin_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
