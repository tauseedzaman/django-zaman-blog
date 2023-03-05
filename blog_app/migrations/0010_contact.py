# Generated by Django 4.1.7 on 2023-03-05 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0009_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('subject', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
