# Generated by Django 3.1.7 on 2021-04-25 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mcu_site', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='date',
        ),
        migrations.AddField(
            model_name='movie',
            name='year',
            field=models.CharField(default=2021, max_length=10),
            preserve_default=False,
        ),
    ]
