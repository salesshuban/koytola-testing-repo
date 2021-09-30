# Generated by Django 3.1 on 2021-06-17 06:18

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import koytola.core.db.fields
import koytola.core.utils
import koytola.core.utils.editorjs
import koytola.core.utils.json_serializer
import versatileimagefield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('private_metadata', models.JSONField(blank=True, default=dict, encoder=koytola.core.utils.json_serializer.CustomJsonEncoder, null=True)),
                ('metadata', models.JSONField(blank=True, default=dict, encoder=koytola.core.utils.json_serializer.CustomJsonEncoder, null=True)),
                ('seo_title', models.CharField(blank=True, max_length=70, null=True, validators=[django.core.validators.MaxLengthValidator(70)])),
                ('seo_description', models.CharField(blank=True, max_length=300, null=True, validators=[django.core.validators.MaxLengthValidator(300)])),
                ('name', models.CharField(max_length=250, unique=True)),
                ('slug', models.SlugField(allow_unicode=True, max_length=255, unique=True)),
                ('description', koytola.core.db.fields.SanitizedJSONField(blank=True, default=dict, sanitizer=koytola.core.utils.editorjs.clean_editor_js)),
                ('description_plaintext', models.TextField(blank=True, default='')),
                ('background_image', versatileimagefield.fields.VersatileImageField(blank=True, null=True, upload_to='category-backgrounds')),
                ('background_image_alt', models.CharField(blank=True, max_length=128)),
                ('tags', models.TextField(blank=True, max_length=25000, null=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='product.category')),
            ],
            options={
                'ordering': ['slug', 'name', 'pk'],
                'permissions': [('manage_categories', 'Manage categories.')],
            },
        ),
        migrations.CreateModel(
            name='HSCodeAndProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hs_code', models.CharField(max_length=250)),
                ('product_name', models.TextField(blank=True, default='')),
            ],
        ),
        migrations.CreateModel(
            name='Offers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=250)),
                ('slug', models.CharField(blank=True, max_length=250)),
                ('get_code', models.CharField(blank=True, max_length=250)),
                ('value', models.IntegerField(default=0)),
                ('unit', models.CharField(choices=[('%', '%'), ('DIRECT', 'DIRECT')], max_length=250)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('tags', models.TextField(default='[]', max_length=65500)),
                ('image', models.ImageField(blank=True, upload_to=koytola.core.utils.upload_path_handler)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('categories', models.ManyToManyField(blank=True, related_name='_offers_categories_+', to='product.Category')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='offers_company', to='profile.company')),
            ],
        ),
        migrations.CreateModel(
            name='PortDeals',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=250)),
                ('slug', models.CharField(blank=True, max_length=250, null=True)),
                ('location', models.TextField(blank=True, max_length=2500)),
                ('product_name', models.TextField(blank=True, max_length=25000, null=True)),
                ('hs_code', models.CharField(max_length=250)),
                ('quantity', models.IntegerField(default=0)),
                ('unit', models.CharField(blank='item', choices=[('centimeter', 'Centi-Meter unit'), ('centimeter-square', 'Centi-Meter Square Unit'), ('centimeter-cube', 'Centi-Meter Cube Unit'), ('gallon', 'Gallon unit'), ('gram', 'Gram unit'), ('item', 'Item unit'), ('kilogram', 'Kilo-Gram unit'), ('lbm', 'Pound unit'), ('liter', 'Liter unit'), ('milligram', 'Milli-Gram unit'), ('millimeter', 'Milli-Meter unit'), ('millimeter-square', 'Milli-Meter Square unit'), ('millimeter-cube', 'Milli-Meter Cube unit'), ('meter', 'Meter unit'), ('meter-square', 'Meter Square Unit'), ('meter-cube', 'Meter Cube unit'), ('ounce', 'Ounce unit'), ('ton', 'Ton unit')], max_length=32, null=True)),
                ('price', models.FloatField(default=0.0)),
                ('discount_price', models.FloatField(default=0.0)),
                ('discount_percentage', models.FloatField(default=0.0)),
                ('certificate', models.TextField(blank=True, max_length=25000, null=True)),
                ('description', models.TextField(blank=True, max_length=65500, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='port_deals_company', to='profile.company')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('publication_date', models.DateField(blank=True, null=True)),
                ('update_date', models.DateField(auto_now=True)),
                ('private_metadata', models.JSONField(blank=True, default=dict, encoder=koytola.core.utils.json_serializer.CustomJsonEncoder, null=True)),
                ('metadata', models.JSONField(blank=True, default=dict, encoder=koytola.core.utils.json_serializer.CustomJsonEncoder, null=True)),
                ('seo_title', models.CharField(blank=True, max_length=70, null=True, validators=[django.core.validators.MaxLengthValidator(70)])),
                ('seo_description', models.CharField(blank=True, max_length=300, null=True, validators=[django.core.validators.MaxLengthValidator(300)])),
                ('name', models.TextField(max_length=25000)),
                ('slug', models.SlugField(allow_unicode=True, max_length=255, unique=True)),
                ('description', koytola.core.db.fields.SanitizedJSONField(blank=True, default=dict, sanitizer=koytola.core.utils.editorjs.clean_editor_js)),
                ('description_plaintext', models.TextField(blank=True, default='')),
                ('hs_code', models.CharField(max_length=32)),
                ('unit_number', models.PositiveIntegerField(default=1)),
                ('unit', models.CharField(blank='item', choices=[('centimeter', 'Centi-Meter unit'), ('centimeter-square', 'Centi-Meter Square Unit'), ('centimeter-cube', 'Centi-Meter Cube Unit'), ('gallon', 'Gallon unit'), ('gram', 'Gram unit'), ('item', 'Item unit'), ('kilogram', 'Kilo-Gram unit'), ('lbm', 'Pound unit'), ('liter', 'Liter unit'), ('milligram', 'Milli-Gram unit'), ('millimeter', 'Milli-Meter unit'), ('millimeter-square', 'Milli-Meter Square unit'), ('millimeter-cube', 'Milli-Meter Cube unit'), ('meter', 'Meter unit'), ('meter-square', 'Meter Square Unit'), ('meter-cube', 'Meter Cube unit'), ('ounce', 'Ounce unit'), ('ton', 'Ton unit')], max_length=32, null=True)),
                ('unit_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('currency', models.CharField(default='USD', max_length=3)),
                ('minimum_order_quantity', models.PositiveIntegerField(default=1)),
                ('organic', models.BooleanField(default=False)),
                ('private_label', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_published', models.BooleanField(default=False)),
                ('is_brand', models.BooleanField(default=False)),
                ('brand', models.CharField(blank=True, max_length=255, null=True)),
                ('tags', models.TextField(blank=True, default='[]', max_length=6550)),
                ('packaging', models.TextField(blank=True, max_length=65500, null=True)),
                ('delivery', models.TextField(blank=True, max_length=65500, null=True)),
                ('delivery_time', models.CharField(blank=True, max_length=255, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='product.category')),
                ('certificate_type', models.ManyToManyField(blank=True, related_name='_product_certificate_type_+', to='profile.CertificateType')),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='profile.company')),
                ('rosetter', models.ManyToManyField(blank=True, related_name='_product_rosetter_+', to='profile.Roetter')),
            ],
            options={
                'ordering': ['slug', 'name', 'pk'],
                'permissions': [('manage_products', 'Manage products.')],
            },
        ),
        migrations.CreateModel(
            name='ProductVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', versatileimagefield.fields.VersatileImageField(upload_to='products')),
                ('alt_text', models.CharField(blank=True, max_length=128)),
                ('order', models.PositiveIntegerField(default=1)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='product.product')),
            ],
            options={
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='ProductReviews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('rating', models.FloatField(default=0)),
                ('review', models.TextField(blank=True, max_length=65500, null=True)),
                ('location', models.TextField(blank=True, max_length=65500, null=True)),
                ('like', models.IntegerField(default=0)),
                ('unlike', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_review', to='product.product')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_review_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProductQuery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('message', models.TextField(default='', max_length=65500)),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2, null=True)),
                ('is_closed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('offer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_query_offer', to='product.offers')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_query', to='product.product')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_query_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', versatileimagefield.fields.VersatileImageField(upload_to='products')),
                ('ppoi', versatileimagefield.fields.PPOIField(default='0.5x0.5', editable=False, max_length=20)),
                ('alt_text', models.CharField(blank=True, max_length=128)),
                ('order', models.PositiveIntegerField(default=1)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='product.product')),
            ],
            options={
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='PortProductGallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', versatileimagefield.fields.VersatileImageField(null=True, upload_to='products/port/')),
                ('ppoi', versatileimagefield.fields.PPOIField(default='0.5x0.5', editable=False, max_length=20)),
                ('video', versatileimagefield.fields.VersatileImageField(null=True, upload_to='products/port/')),
                ('alt_text', models.CharField(blank=True, max_length=128)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='port_product_gallery', to='product.portdeals')),
            ],
        ),
        migrations.AddField(
            model_name='offers',
            name='products',
            field=models.ManyToManyField(blank=True, related_name='_offers_products_+', to='product.Product'),
        ),
        migrations.AddField(
            model_name='offers',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='offers_user', to=settings.AUTH_USER_MODEL),
        ),
    ]