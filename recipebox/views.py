from django.contrib.auth.models import User
from django.shortcuts import render

from recipebox.models import Recipe, Author
from recipebox.forms import RecipeAddForm
from recipebox.forms import AuthorAddForm


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


def recipe_add(request):
    html = 'recipe_add.html'
    form = None

    if request.method == 'POST':
        form = RecipeAddForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            new_recipe = Recipe.objects.create(
                title=data['title'],
                instructions=data['instructions'],
                author=data['author'],
                description=data['description'],
                time_required=data['time_required']
            )
            return render(request, 'thanks.html', {'new_recipe': new_recipe})

    else:
        form = RecipeAddForm()
    return render(request, html, {'form': form})


def author_add(request):
    html = 'author_add.html'
    form = None

    if request.method == 'POST':
        form = AuthorAddForm(request.POST)
        
        if form.is_valid():
            data = form.cleaned_data

            user = User.objects.create_user(username=data['name'])

            author = Author.objects.create(
                user=user,
                name=data['name'],
                bio=data['bio'],
                )

            return render(request, 'welcome.html', {'new_user': author})
    else:
        form = AuthorAddForm()

    return render(request, html, {'hi': form})

