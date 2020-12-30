# Generated by Django 3.1.2 on 2020-12-11 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='swiped',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stime', models.DateTimeField(auto_created=True, verbose_name='滑动时间')),
                ('uid', models.ImageField(upload_to='', verbose_name='用户 ID')),
                ('sid', models.ImageField(upload_to='', verbose_name='被滑动用户的ID')),
                ('stype', models.CharField(max_length=10)),
            ],
            options={
                'unique_together': {('uid', 'sid')},
            },
        ),
    ]
