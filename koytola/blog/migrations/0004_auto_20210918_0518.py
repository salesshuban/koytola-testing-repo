# Generated by Django 3.1 on 2021-09-18 05:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_blogimages'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'ordering': ['-created_at'], 'permissions': [('manage_blogs', 'Manage blogs.')]},
        ),
    ]