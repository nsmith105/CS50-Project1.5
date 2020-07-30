from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def view_page(request, title):
    file_name = util.search_for_file(request, title)

    content = util.md_to_html(file_name)

    