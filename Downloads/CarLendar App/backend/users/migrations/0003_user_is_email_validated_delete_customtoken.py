# Generated by Django 4.2.6 on 2023-10-15 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_created_at_customtoken'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_email_validated',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='CustomToken',
        ),
    ]