# Generated by Django 5.1.6 on 2025-02-15 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bus_id', models.IntegerField()),
                ('route', models.IntegerField()),
                ('passengers', models.IntegerField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'unique_together': {('bus_id', 'timestamp')},
            },
        ),
    ]
