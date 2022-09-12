# Generated by Django 4.1 on 2022-09-06 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='postnews',
            name='free',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='postnews',
            name='description',
            field=models.TextField(blank=True, max_length=200),
        ),
    ]