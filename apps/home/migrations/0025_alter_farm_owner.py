# Generated by Django 4.2.2 on 2024-05-15 10:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0024_result_tree'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farm',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='farms', to=settings.AUTH_USER_MODEL),
        ),
    ]
