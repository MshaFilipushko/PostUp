# Generated by Django 4.2.18 on 2025-01-28 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('draft', 'Черновик'), ('published', 'Опубликовано')], default='draft', max_length=10),
        ),
    ]
