# Generated by Django 4.2.8 on 2023-12-14 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_user_tc'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='otp',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='tc',
            field=models.CharField(max_length=11, unique=True),
        ),
    ]
