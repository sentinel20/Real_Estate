# Generated by Django 3.2 on 2022-08-25 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='listings',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
    ]
