# Generated by Django 4.2.2 on 2023-12-26 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_alter_packetresult_direction_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='packetresult',
            name='AirTC_AvgUnit',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='packetresult',
            name='AirTC_MaxUnit',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='packetresult',
            name='AirTC_MinUnit',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='packetresult',
            name='AirTC_TMnUnit',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='packetresult',
            name='AirTC_TMxUnit',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='packetresult',
            name='BP_mmHg_AvgUnit',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='packetresult',
            name='BattV_AvgUnit',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='packetresult',
            name='BattV_MinUnit',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='packetresult',
            name='PTemp_C_AvgUnit',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='packetresult',
            name='RHUnit',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='packetresult',
            name='Rain_mm_TotUnit',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='packetresult',
            name='SlrMJ_TotUnit',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='packetresult',
            name='SlrkW_AvgUnit',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='packetresult',
            name='Visibility_m_AvgUnit',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='packetresult',
            name='wind_speed_AVGUnit',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
