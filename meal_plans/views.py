from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from meal_plans.models import MealPlan

# Create your views here.


class MealPlanListView(LoginRequiredMixin, ListView):
    model = MealPlan
    template_name = "meal_plans/list.html"

    def get_queryset(self):
        return MealPlan.objects.filter(owner=self.request.user)


class MealPlanCreateView(LoginRequiredMixin, CreateView):
    model = MealPlan
    template_name = "meal_plans/new.html"
    fields = ["name", "date", "recipes"]
    success_url = reverse_lazy("meal_plan_list")
    # customization of saving the form
    def form_valid(self, form):
        # save the meal plan BUT do not put it in the
        # database(get the instances from form but only in memory not in database)
        plan = form.save(commit=False)
        # assign the owner to the meal plan
        plan.owner = self.request.user
        # now save it to the database
        plan.save()
        # save all of the m2m relationships
        form.save_m2m()
        # redirecting to the detail page for meal plan
        return redirect("meal_plan_detail", pk=plan.id)

    # def form_valid(self, form):
    #     form.instance.author = self.request.user
    #     return super().form_valid(form)


class MealPlanDetailView(DetailView):
    model = MealPlan
    template_name = "meal_plans/detail.html"

    def get_queryset(self):
        return MealPlan.objects.filter(owner=self.request.user)


class MealPlanUpdateView(LoginRequiredMixin, UpdateView):
    model = MealPlan
    template_name = "meal_plans/edit.html"
    fields = ["name", "date", "owner", "recipes"]
    success_url = reverse_lazy("meal_plan_list")

    def get_queryset(self):
        return MealPlan.objects.filter(owner=self.request.user)


class MealPlanDeleteView(LoginRequiredMixin, DeleteView):
    model = MealPlan
    template_name = "meal_plans/delete.html"
    success_url = reverse_lazy("meal_plan_list")

    def get_queryset(self):
        return MealPlan.objects.filter(owner=self.request.user)
