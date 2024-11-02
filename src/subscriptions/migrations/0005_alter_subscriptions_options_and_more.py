# Generated by Django 5.0.9 on 2024-10-22 17:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("subscriptions", "0004_subscriptions_permissions"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="subscriptions",
            options={
                "permissions": [
                    ("advanced", "Advanced Perm"),
                    ("pro", "Pro Perm"),
                    ("basic", "Basic Perm"),
                ]
            },
        ),
        migrations.AlterField(
            model_name="subscriptions",
            name="permissions",
            field=models.ManyToManyField(
                limit_choices_to={
                    "codename__in": ["advanced", "pro", "basic"],
                    "content_type__app_label": "subscriptions",
                },
                to="auth.permission",
            ),
        ),
    ]
