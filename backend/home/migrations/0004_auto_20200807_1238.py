# Generated by Django 3.0.3 on 2020-08-07 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_payment_checkout_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passengeraccount',
            name='lastname',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]