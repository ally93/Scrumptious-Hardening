from sqlite3 import IntegrityError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from recipes.forms import RatingForm
from recipes.models import Ingredient, Recipe, ShoppingItem
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_http_methods


def log_rating(request, recipe_id):
    try:
        if request.method == "POST":
            form = RatingForm(request.POST)
            if form.is_valid():
                rating = form.save(commit=False)
                rating.recipe = Recipe.objects.get(pk=recipe_id)
                rating.save()
        return redirect("recipe_detail", pk=recipe_id)
    except Recipe.DoesNotExist:
        return redirect("recipes_list")


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

        shopping_list = []
        for item in self.request.user.shoppingitems.all():
            shopping_list.append(item.food_item)

        context["servings"] = self.request.GET.get("servings")

        context["fooditems"] = shopping_list
        return context


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    template_name = "recipes/new.html"
    fields = ["name", "description", "image", "servings"]
    success_url = reverse_lazy("recipes_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipe
    template_name = "recipes/edit.html"
    fields = ["name", "author", "description", "image", "servings"]
    success_url = reverse_lazy("recipes_list")


class RecipeDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipe
    template_name = "recipes/delete.html"
    success_url = reverse_lazy("recipes_list")


class ShoppingItemListView(LoginRequiredMixin, ListView):
    model = ShoppingItem
    template_name = "shoppingitems/list.html"
    success_url = reverse_lazy("shoppingitems_list")

    def get_queryset(self):
        return ShoppingItem.objects.filter(user=self.request.user)


@require_http_methods(["POST"])
def create_shopping_item(request):
    # get ingredient id from post request
    ingredient_id = request.POST.get("ingredient_id")
    ingredient = Ingredient.objects.get(id=ingredient_id)
    # get user id
    requested_user = request.user

    try:
        # create shopping list item
        ShoppingItem.objects.create(
            user=requested_user, food_item=ingredient.food
        )
    except IntegrityError:
        pass
    # redirect to current recipe page-which we get from the request
    return redirect("recipe_detail", pk=ingredient.recipe.id)


@require_http_methods(["POST"])
def delete_shopping_item(request):
    ShoppingItem.objects.filter(user=request.user).delete()
    return redirect("shoppingitems_list")
