# Generated by Django 2.2.1 on 2019-05-24 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipebox', '0003_auto_20190503_1404'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='favorites',
            field=models.ManyToManyField(blank=True, related_name='favorites', to='recipebox.Recipe'),
        ),
    ]