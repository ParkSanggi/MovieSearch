# Generated by Django 2.1 on 2019-05-16 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0002_movie_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='movie',
            name='director',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
