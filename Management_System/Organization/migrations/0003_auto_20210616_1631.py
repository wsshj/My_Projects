# Generated by Django 3.1.7 on 2021-06-16 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Organization', '0002_auto_20210616_1544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='number',
            field=models.CharField(max_length=10),
        ),
    ]
