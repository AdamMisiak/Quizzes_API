# Generated by Django 4.1 on 2022-10-03 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attempts', '0003_remove_attemptanswer_modified_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='attemptanswer',
            name='is_correct',
            field=models.BooleanField(default=False, verbose_name='is_correct'),
        ),
    ]
