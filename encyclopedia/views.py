from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django import forms
import numpy as np

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def existing_entry(request, title):
    return render (request, "encyclopedia/content.html", {
        "title": title,
        "content": util.get_entry(title.upper())
    })

class CreateNewPage(forms.Form):
    title = forms.CharField()
    textarea = forms.CharField(widget=forms.Textarea(attrs={ 'cols': 80, 'rows': 10 }))

def new_page(request):
    if request.method == 'POST':
        form = CreateNewPage(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleand_data['textarea']
            util.save_entry(title, content)

    return render(request, "encyclopedia/newpage.html", {
        "form": CreateNewPage()
    })

def random_page(request):
    n = np.random.randint(1,len(util.list_entries()))
    title = util.list_entries()[n]
    return render(request, "encyclopedia/content.html", {
        "title": title,
        "content": util.get_entry(title)
    })

