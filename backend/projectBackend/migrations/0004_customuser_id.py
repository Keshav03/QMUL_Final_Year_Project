# Generated by Django 4.0.2 on 2022-05-02 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectBackend', '0003_profile_profile_firstname_profile_profile_lastname_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='id',
            field=models.IntegerField(null=True),
        ),
    ]
