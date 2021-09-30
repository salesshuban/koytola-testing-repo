# Generated by Django 3.1 on 2021-08-03 12:37

from django.db import migrations
import koytola.core.utils
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0003_auto_20210723_0542'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificatetype',
            name='image',
            field=versatileimagefield.fields.VersatileImageField(blank=True, null=True, upload_to=koytola.core.utils.upload_path_handler),
        ),
    ]