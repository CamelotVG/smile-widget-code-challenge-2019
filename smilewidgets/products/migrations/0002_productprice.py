# Generated by Django 2.0.7 on 2019-09-18 07:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(help_text='Name of event', max_length=40)),
                ('date_start', models.DateField()),
                ('date_end', models.DateField(blank=True, null=True)),
                ('price', models.PositiveIntegerField(help_text='Special price of product in cents')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_prices', to='products.Product', verbose_name='Product')),
            ],
        ),
    ]
