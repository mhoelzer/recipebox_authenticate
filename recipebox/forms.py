from django import forms
# from recipebox.models import Author


# Make two new html pages for our recipe application: one to add recipes, and one to add authors
class RecipeAddForm(forms.Form):
    title = forms.CharField(max_length=160)
    instructions = forms.CharField(widget=forms.Textarea)
    # author = forms.ModelChoiceField(queryset=Author.objects.all())
    description = forms.CharField(max_length=100)
    time_required = forms.CharField(max_length=20)


class AuthorAddForm(forms.Form):
    name = forms.CharField(max_length=50)
    bio = forms.CharField(widget=forms.Textarea)


class SignupForm(forms.Form):
    name = forms.CharField(max_length=100)
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    bio = forms.CharField(widget=forms.Textarea)
    password = forms.CharField(widget=forms.PasswordInput())


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())