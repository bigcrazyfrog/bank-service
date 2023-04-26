# Generated by Django 4.2 on 2023-04-26 15:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='IssuedToken',
            new_name='RefreshToken',
        ),
        migrations.CreateModel(
            name='AccessToken',
            fields=[
                ('jti', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('revoked', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='access_token', to='app.user')),
            ],
        ),
    ]
