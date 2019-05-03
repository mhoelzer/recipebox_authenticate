from django.shortcuts import render

from recipebox.models import Recipe
from recipebox.models import Author


def index(request):
    html = "index.html"
    recipes = Recipe.objects.all()
    return render(request, html, {'data': recipes})


def recipe(request, id):
    html = "recipe.html"    
    recipes = Recipe.objects.filter(id=id)
    return render(request, html, {'data': recipes})


def auth_detail(request, id):
    html = "author.html"
    author = Author.objects.filter(id=id)
    list_of_recipes = Recipe.objects.filter(author_id=id)
    return render(request, html, {'data': author, 'recipes': list_of_recipes})