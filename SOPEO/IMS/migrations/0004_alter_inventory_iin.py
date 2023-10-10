# Generated by Django 4.1.2 on 2023-09-16 12:28

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('IMS', '0003_transaction_orders'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='iin',
            field=models.UUIDField(default=uuid.uuid1, null=True, unique=True),
        ),
    ]
