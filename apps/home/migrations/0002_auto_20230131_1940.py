# Generated by Django 3.2.6 on 2023-01-31 19:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='sensor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='number_results', to='home.sensor'),
        ),
        migrations.AlterField(
            model_name='stringresult',
            name='sensors',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='STRINGRESULT', to='home.sensor'),
        ),
    ]
