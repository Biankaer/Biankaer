# Generated by Django 4.0.2 on 2022-07-04 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ss', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ahau',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('url', models.TextField()),
                ('text', models.TextField()),
                ('ss_date', models.DateField()),
                ('source', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='rsc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('url', models.TextField()),
                ('text', models.TextField()),
            ],
        ),
    ]
