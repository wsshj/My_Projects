# Generated by Django 3.1.7 on 2021-06-29 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Organization', '0004_auto_20210629_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='phone',
            field=models.CharField(max_length=11),
        ),
    ]