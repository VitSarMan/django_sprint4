# Generated by Django 3.2.16 on 2024-08-29 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_alter_post_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='text',
            field=models.TextField(verbose_name='Комментарий'),
        ),
    ]
