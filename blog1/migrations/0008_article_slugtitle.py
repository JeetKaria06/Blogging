# Generated by Django 3.2.3 on 2021-05-26 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog1', '0007_remove_article_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='slugtitle',
            field=models.SlugField(default=''),
        ),
    ]
