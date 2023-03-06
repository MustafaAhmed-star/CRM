# Generated by Django 4.1.6 on 2023-03-06 19:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("leads", "0003_user_is_agent_user_is_oraganisor"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lead",
            name="agent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="leads.agent",
            ),
        ),
    ]
