# Generated by Django 3.2.6 on 2023-03-06 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20230227_2110'),
    ]

    operations = [
        migrations.AddField(
            model_name='farm',
            name='farmName',
            field=models.CharField(default='MyFarm', max_length=200),
        ),
    ]