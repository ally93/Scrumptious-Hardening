from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.list import ListView

from meal_plans.models import MealPlan

# Create your views here.


class MealPlanListView(ListView):
    model = MealPlan
    template_name = "meal_plans/list.html"
