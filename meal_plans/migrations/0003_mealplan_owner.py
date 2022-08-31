# Generated by Django 4.0.3 on 2022-08-31 22:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('meal_plans', '0002_mealplan_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='mealplan',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='meal_plan', to=settings.AUTH_USER_MODEL),
        ),
    ]
