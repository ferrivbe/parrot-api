# Generated by Django 3.2.8 on 2021-12-10 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0004_alter_productquantity_order"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="closed_at",
            field=models.DateTimeField(default=None, null=True),
        ),
    ]
