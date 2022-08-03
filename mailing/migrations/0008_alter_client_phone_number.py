# Generated by Django 4.0.6 on 2022-07-30 16:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0007_alter_client_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='phone_number',
            field=models.CharField(max_length=11, unique=True, validators=[django.core.validators.RegexValidator('\\b7[0-9]{10}\\b'), django.core.validators.MinLengthValidator(11)]),
        ),
    ]
