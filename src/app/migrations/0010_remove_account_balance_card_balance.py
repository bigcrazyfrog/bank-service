# Generated by Django 4.2b1 on 2023-03-28 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_rename_account_number_card_account'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='balance',
        ),
        migrations.AddField(
            model_name='card',
            name='balance',
            field=models.BigIntegerField(default=0, verbose_name='Balance'),
        ),
    ]
