# Generated by Django 4.2 on 2024-05-23 17:03

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("library", "0003_alter_library_options_alter_rack_book_copy"),
        ("book", "0004_bookcopy_order_alter_bookcopy_book"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="bookcopy",
            unique_together={("library", "book", "order")},
        ),
    ]