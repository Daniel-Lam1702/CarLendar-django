# Generated by Django 4.2.6 on 2023-10-09 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=129)),
                ('email', models.CharField(max_length=320)),
                ('biography', models.TextField()),
                ('profile_picture', models.BinaryField()),
                ('created_at', models.DateTimeField()),
                ('last_online', models.DateTimeField()),
            ],
        ),
    ]
