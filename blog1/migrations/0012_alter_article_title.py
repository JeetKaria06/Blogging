# Generated by Django 3.2.3 on 2021-05-26 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog1', '0011_remove_article_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]