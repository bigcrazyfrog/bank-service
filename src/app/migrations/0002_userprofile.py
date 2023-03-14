# Generated by Django 4.2a1 on 2023-02-15 18:49

import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_id', models.PositiveIntegerField(unique=True, verbose_name='telegram ID')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='phone number')),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Профиль',
            },
        ),
    ]
