import re
import markdown2 as MD
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponse


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None

def md_to_html(filename):
    """
    Converts markdown to HTML for the render function
    """

    converter = MD.Markdown()
    try:
        f = get_entry(filename)
    except:
        f = f'{file_name} not found!'
    return converter.convert(f)

def search_for_file(request, title):
    """
    Search function used for page search
    """

    f_name = ""
    entries = list_entries()

    # first check if page is valid, render 404 if not
    if title.casefold() not in (entry.casefold() for entry in entries):
        context = {
            "name": title
        }
        return render(request, "encyclopedia/page_not_found.html", context)

    # return found page from list     
    else:
        for entry in entries:
            if entry.casefold() == title:
                file_name = entry
    
    return file_name