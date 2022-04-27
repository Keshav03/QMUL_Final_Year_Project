# Generated by Django 4.0.2 on 2022-03-13 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectBackend', '0003_customuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='firstName',
        ),
        migrations.RemoveField(
            model_name='user',
            name='lastName',
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='email address'),
        ),
    ]