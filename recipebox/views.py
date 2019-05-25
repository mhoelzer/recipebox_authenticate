from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import reverse, render

from recipebox.models import Recipe, Author
from recipebox.forms import RecipeAddForm
# add author form is a form to be used solely by the admin to add an author
from recipebox.forms import AuthorAddForm
from recipebox.forms import SignupForm
from recipebox.forms import LoginForm
from recipebox.forms import RecipeUpdateForm


def index(request):
    html = "index.html"
    recipes = Recipe.objects.all()
    return render(request, html, {'data': recipes})


def recipe(request, id):
    html = "recipe.html"
    recipes = Recipe.objects.get(id=id)
    current_user = request.user
    fav_button = None
    show_edit_button = None
    if current_user.is_authenticated:
        if request.user.author == recipes.author or current_user.is_staff:
            show_edit_button = True
        if recipes not in current_user.author.favorites.all():
            fav_button = "love it!"
        elif recipes in current_user.author.favorites.all():
            fav_button = "this sucks; i hate it"
    else:
        show_edit_button = False
        return render(request, html, {'data': recipes,
                                      "show_edit_button": show_edit_button})
    return render(request, html, {'data': recipes,
                                  "fav_button": fav_button,
                                  "show_edit_button": show_edit_button})


def favorite_status(request, id):
    html = "../templates/favorite_status.html"
    is_favorite = False
    current_user = request.user
    recipe = Recipe.objects.filter(id=id).first()
    if recipe not in current_user.author.favorites.get_queryset():
        current_user.author.favorites.add(recipe)
        is_favorite = True
    else:
        current_user.author.favorites.remove(recipe)
        is_favorite = False
    current_user.save()
    return render(request, html, {"is_favorite": is_favorite})


def auth_detail(request, id):
    html = "author.html"
    author = Author.objects.filter(id=id)
    list_of_recipes = Recipe.objects.filter(author_id=id)
    favorites = author.first().favorites.get_queryset()
    return render(request, html, {'data': author,
                                  'recipes': list_of_recipes,
                                  "favorites": favorites})


@login_required()
def recipe_add(request):
    html = 'recipe_add.html'
    form = None
    # show_edit_button: False
    if request.method == 'POST':
        form = RecipeAddForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            new_recipe = Recipe.objects.create(
                title=data['title'],
                instructions=data['instructions'],
                # author=data['author'],
                author=request.user.author,
                description=data['description'],
                time_required=data['time_required']
            )
            # show_edit_button = True
            return render(request, 'thanks.html', {'new_recipe': new_recipe})

    else:
        form = RecipeAddForm()
        # show_edit_button = False
    return render(request, html, {'form': form})


@login_required()
# if currentuser is recipe author
def recipe_update(request, id):
    html = 'recipe_update.html'
    form = None
    current_user = User.objects.get(id=request.user.id)
    current_recipe = Recipe.objects.get(id=id)
    data = {
        "title": current_recipe.title,
        "description": current_recipe.description,
        "time_required": current_recipe.time_required,
        "instructions": current_recipe.instructions,
    }
    # if current_user or request.user.is_authenticated or request.auth:
    # could also put this around the button in the recipe.html
    if request.method == 'POST':
        form = RecipeUpdateForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            current_recipe.title = data['title']
            current_recipe.instructions = data['instructions']
            current_recipe.description = data['description']
            current_recipe.time_required = data['time_required']
            current_recipe.save()
            # return HttpResponseRedirect(reverse('index'))
            return render(request, 'updated.html', {'current_recipe': current_recipe})
    else:
        form = RecipeUpdateForm(initial=data)
        # form.fields["title"].initial = current_recipe.title
    return render(request, html, {'form': form})

# author add is for admin to add an author
@login_required()
@staff_member_required()
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


def signup_view(request):
    html = "generic_form.html"
    form = None

    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                data['username'], data['email'], data['password'])
            login(request, user)
            Author.objects.create(
                name=data['name'],
                bio=data["bio"],
                user=user
            )
            return HttpResponseRedirect(reverse('index'))
    else:
        form = SignupForm()
    return render(request, html, {'form': form})


def login_view(request):
    html = "generic_form.html"
    form = None

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                username=data['username'], password=data['password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', '/'))

    else:
        form = LoginForm()
    return render(request, html, {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
