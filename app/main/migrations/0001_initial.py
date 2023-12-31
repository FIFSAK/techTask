# Generated by Django 4.2.4 on 2023-08-21 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('extension', models.CharField(blank=True, max_length=10)),
                ('MIME_type', models.CharField(max_length=50)),
                ('size', models.PositiveIntegerField()),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_or_email', models.CharField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=50)),
            ],
        ),
    ]
