# Generated by Django 3.1.5 on 2021-04-12 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_customer_profile_pic'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shares', models.FloatField(null=True)),
                ('savings', models.FloatField(null=True)),
                ('loan', models.FloatField(null=True)),
                ('rss', models.FloatField(null=True)),
                ('buildingfund', models.FloatField(null=True)),
                ('investment1', models.FloatField(null=True)),
                ('investment2', models.FloatField(null=True)),
            ],
        ),
    ]
