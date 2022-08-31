# Generated by Django 4.0.3 on 2022-08-31 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0009_recipe_author'),
        ('meal_plans', '0003_mealplan_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='mealplan',
            name='recipes',
            field=models.ManyToManyField(related_name='meal_plans', to='recipes.recipe'),
        ),
    ]