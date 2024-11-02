# Generated by Django 5.0.9 on 2024-10-22 23:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("subscriptions", "0010_rename_subscriptions_subscription_subscriptionprice"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="subscriptionprice",
            name="active",
        ),
        migrations.RemoveField(
            model_name="subscriptionprice",
            name="groups",
        ),
        migrations.RemoveField(
            model_name="subscriptionprice",
            name="name",
        ),
        migrations.RemoveField(
            model_name="subscriptionprice",
            name="permissions",
        ),
        migrations.AddField(
            model_name="subscriptionprice",
            name="interval",
            field=models.CharField(
                choices=[("monthly", "Monthly"), ("yearly", "Yearly")],
                default="monthly",
                max_length=120,
            ),
        ),
        migrations.AddField(
            model_name="subscriptionprice",
            name="price",
            field=models.DecimalField(decimal_places=2, default=99.99, max_digits=10),
        ),
        migrations.AddField(
            model_name="subscriptionprice",
            name="subscription",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="subscriptions.subscription",
            ),
        ),
    ]
