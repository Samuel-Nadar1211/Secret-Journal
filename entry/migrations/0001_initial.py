# Generated by Django 5.0.6 on 2024-06-15 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Entries",
            fields=[
                ("entry_id", models.AutoField(primary_key=True, serialize=False)),
                ("user_id", models.IntegerField()),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=25)),
                ("content", models.TextField()),
            ],
        ),
    ]
