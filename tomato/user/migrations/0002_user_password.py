# Generated by Django 3.1.2 on 2020-11-04 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(default='123', max_length=254, verbose_name='密码'),
        ),
    ]
