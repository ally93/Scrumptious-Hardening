from django.urls import path

from meal_plans.views import (
    MealPlanListView
)

urlpatterns = [
    path("", MealPlanListView.as_view(), name="meal_plans_list"),
    # path("<int:pk>/", RecipeDetailView.as_view(), name="recipe_detail"),
    # path("<int:pk>/delete/", RecipeDeleteView.as_view(), name="recipe_delete"),
    # path("new/", RecipeCreateView.as_view(), name="recipe_new"),
    # path("<int:pk>/edit/", RecipeUpdateView.as_view(), name="recipe_edit"),
    # path("<int:recipe_id>/ratings/", log_rating, name="recipe_rating"),
]
