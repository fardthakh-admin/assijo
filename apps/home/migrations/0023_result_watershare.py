# Generated by Django 4.2.2 on 2024-04-24 19:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0022_home_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='watershare',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='number_results', to='home.watershare'),
        ),
    ]