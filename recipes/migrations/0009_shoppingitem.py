# Generated by Django 4.0.3 on 2022-09-05 01:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0008_recipe_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShoppingItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='recipes.fooditem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shoppingitems', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
