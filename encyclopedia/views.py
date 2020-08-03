from django.shortcuts import render
from markdown2 import markdown
from random import choice

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def view_page(request, title):
    content = util.get_entry(title)
    if not content:
        return render(request, "encyclopedia/page_not_found.html", {
            "message": "\"" + title + "\" has no entry. Maybe you should create one? :)"
        })
    return render(request, "encyclopedia/view_page.html", {
        "title": title, 
        "content": markdown(content)
    })

def search(request):
    keyword = request.GET.get("q")
    content = util.get_entry(keyword)
    if not content:
        result = []
        for title in util.list_entries():
            if keyword.casefold() in title.casefold():
                result.appent(title)
        return render(request, "encyclopedia/search.html", {
            "result": result
        })
    return render(request, "encyclopedia/view_page.html", {
        "title": keyword, 
        "content": markdown(content)
    })

def new_page(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        for entry in util.list_entries():
            if title.casefold() == entry.casefold():
                return render(request, "encyclopedia/new_page.html", {
                    "message": "Your entry already exists!",
                    "title": title,
                    "content": content
                })
        util.save_entry(title, content)
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "message": "New entry successfully added"
        })
    return render(request, "encyclopedia/new_page.html")

def edit_page(request, title):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        util.save_entry(title, content)
        return render(request, "encyclopedia/entry.html", {
            "title": title, 
            "content": markdown(content),
            "message": "\"" + title + "\" has been successfully updated"
        })
    content = util.get_entry(title)
    return render(request, "encyclopedia/edit_page.html", {
        "title": title, 
        "content": content
    })

def random_page(request):
    title = choice(util.list_entries())
    content = util.get_entry(title)
    return render(request, "encyclopedia/view_page.html", {
        "title": title, 
        "content": markdown(content)
    })
