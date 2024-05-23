# Generated by Django 4.2 on 2024-05-23 05:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("library", "0002_rack"),
        ("user", "0002_userlibraryrelation_customuser_libraries"),
    ]

    operations = [
        migrations.AddField(
            model_name="userlibraryrelation",
            name="max_num_books",
            field=models.IntegerField(default=5),
        ),
        migrations.AlterField(
            model_name="userlibraryrelation",
            name="library",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_relations",
                to="library.library",
            ),
        ),
        migrations.AlterField(
            model_name="userlibraryrelation",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="library_relations",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
