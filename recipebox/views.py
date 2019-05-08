from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import reverse, render

from recipebox.models import Recipe, Author
from recipebox.forms import RecipeAddForm
# add author form is a form to be used solely by the admin to add an author
from recipebox.forms import AuthorAddForm
from recipebox.forms import SignupForm
from recipebox.forms import LoginForm


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


@login_required()
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
                # author=data['author'],
                author=request.user.author,
                description=data['description'],
                time_required=data['time_required']
            )
            return render(request, 'thanks.html', {'new_recipe': new_recipe})

    else:
        form = RecipeAddForm()
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


@login_required()
@staff_member_required()
def signup_view(request):
    html = "generic_form.html"
    form = None

    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                data['username'], data['email'], data['password'])
                # user.save()
            login(request, user)
            Author.objects.create(
                name=data['name'],
                user=user
            )
            return HttpResponseRedirect(reverse('index'))
    else:
        form = SignupForm()
    return render(request, html, {'form': form})

    # recipes = Recipe.objects.all()
    # return render(request, html, {'data': recipes})


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


def logout(request):
    logout(request)
    html = "goodbye.html"
    return render(request, html)
