# Generated by Django 4.0.3 on 2022-08-31 19:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_alter_recipe_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='author',
        ),
    ]
