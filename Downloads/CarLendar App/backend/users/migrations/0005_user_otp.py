# Generated by Django 4.2.6 on 2023-10-22 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_biography_alter_user_last_online_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='otp',
            field=models.CharField(default=0, max_length=6),
            preserve_default=False,
        ),
    ]
