# Generated by Django 3.2.9 on 2023-07-05 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_app', '0002_todoitem_priority'),
    ]

    operations = [
        migrations.AddField(
            model_name='todoitem',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
    ]
