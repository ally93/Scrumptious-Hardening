from sqlite3 import IntegrityError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from recipes.forms import RatingForm
from recipes.models import Ingredient

# try:
#     from recipes.forms import RecipeForm
#     from recipes.models import Recipe
# except Exception:
#     RecipeForm = None
#     Recipe = None

from recipes.models import Recipe, ShoppingItem


def log_rating(request, recipe_id):
    if request.method == "POST":
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            try:
                rating.recipe = Recipe.objects.get(pk=recipe_id)
            except Recipe.DoesNotExist:
                return redirect("recipes_list")
            rating.save()
    return redirect("recipe_detail", pk=recipe_id)


class RecipeListView(ListView):
    model = Recipe
    template_name = "recipes/list.html"
    paginate_by = 2


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = "recipes/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["rating_form"] = RatingForm()
        return context


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    template_name = "recipes/new.html"
    fields = ["name", "description", "image"]
    success_url = reverse_lazy("recipes_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipe
    template_name = "recipes/edit.html"
    fields = ["name", "author", "description", "image"]
    success_url = reverse_lazy("recipes_list")


class RecipeDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipe
    template_name = "recipes/delete.html"
    success_url = reverse_lazy("recipes_list")


# class ShoppingItemCreateView(LoginRequiredMixin, CreateView):
#     model = ShoppingItem
#     template_name: "shopping_items/new.html"
#     success_url: reverse_lazy("recipes_list")


def create_shopping_item(request):
    ingredient_id = request.POST.get("ingredient_id")
    ingredient = Ingredient.objects.get(id=ingredient_id)
    user = request.user

    try:
        ShoppingItem.objects.create(
            food_item=ingredient.food,
            user=user,
        )
    except IntegrityError:
        pass
    return redirect("recipe_detail", pk=ingredient.recipe.id)

class ShoppingItemListView(LoginRequiredMixin, ListView):
    model = ShoppingItem
    template_name = "shopping_items/list.html"

    def get_queryset(self):
        return ShoppingItem.objects.filter(user=self.request.user)

def delete_all_shopping_items(request):
    ShoppingItem.objects.filter(user=request.user).delete()
    return redirect("shopping_item_list")
