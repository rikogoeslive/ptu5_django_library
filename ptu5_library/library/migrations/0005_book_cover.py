# Generated by Django 4.1.3 on 2022-11-14 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_alter_author_options_alter_book_author_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to='covers', verbose_name='cover'),
        ),
    ]
