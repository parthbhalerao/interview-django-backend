# Generated by Django 5.0.9 on 2024-10-22 23:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("subscriptions", "0011_remove_subscriptionprice_active_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usersubscription",
            name="subscription",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="subscriptions.subscription",
            ),
        ),
    ]
