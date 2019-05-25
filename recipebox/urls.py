"""recipebox URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
# from django.urls import include
from recipebox import views

from recipebox.models import Author
from recipebox.models import Recipe

# the lines below tell the admin site that the models exist and that we want to interact with them.  normally in an admin.py file
admin.site.register(Author)
admin.site.register(Recipe)

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('author/<int:id>/', views.auth_detail),
    path('recipe/<int:id>/', views.recipe),
    path('recipeadd/', views.recipe_add),
    path('recipeupdate/<int:id>/', views.recipe_update),
    path('favoritestatus/<int:id>/', views.favorite_status),
    path('authoradd/', views.author_add,),
    path('signup/', views.signup_view),
    path('login/', views.login_view),
    path('logout/', views.logout_view)

]
