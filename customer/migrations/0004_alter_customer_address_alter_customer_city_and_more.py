# Generated by Django 5.2 on 2025-04-12 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_rename_user_customer_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='address',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='city',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='customer',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='state',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='customer',
            name='zip_code',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
