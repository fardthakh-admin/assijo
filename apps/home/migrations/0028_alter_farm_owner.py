# Generated by Django 4.2.2 on 2024-05-15 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0027_alter_farm_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farm',
            name='owner',
            field=models.IntegerField(),
        ),
    ]
