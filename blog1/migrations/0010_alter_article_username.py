# Generated by Django 3.2.3 on 2021-05-26 16:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog1', '0009_article_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog1.author'),
        ),
    ]
