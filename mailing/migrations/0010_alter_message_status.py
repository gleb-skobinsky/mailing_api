# Generated by Django 4.0.6 on 2022-08-01 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0009_alter_client_mobile_code_alter_mailing_mobile_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='status',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
