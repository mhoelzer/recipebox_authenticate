from django.shortcuts import render

from recipebox.models import Recipe


def index(request):

    html = "index.html"

    recipes = Recipe.objects.all()

    return render(request, html, {'data': recipes})