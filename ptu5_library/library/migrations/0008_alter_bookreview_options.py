# Generated by Django 4.1.3 on 2022-11-17 11:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0007_alter_book_summary_bookreview'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookreview',
            options={'ordering': ('-created_at',)},
        ),
    ]
