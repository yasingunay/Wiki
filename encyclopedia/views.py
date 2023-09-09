from django.shortcuts import render, redirect
from django.http import HttpResponse
from .util import markdown_to_html
from .util import get_entry, separate_markdown_content, list_entries

import markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    # If an entry is requested that does not exist, 
    # the user should be presented with an error page indicating that their requested page was not found.
    if not get_entry(title):
        return render(request, "encyclopedia/error.html")
    else:
       #  If the entry does exist, the user should be presented with a page that displays the content of the entry. 
        html_content = markdown_to_html(title)
        header, main_content = separate_markdown_content(html_content)
        return render(request, "encyclopedia/entry.html", {"header": header, "main_content": main_content, "title" : title})  # The title of the page should include the name of the entry.
    
        
def search(request):
    if request.method == "POST":
        title = request.POST["q"]
        # If the query matches the name of an encyclopedia entry, the user should be redirected to that entry’s page.
        if title in list_entries():
            html_content = markdown_to_html(title)
            header, main_content = separate_markdown_content(html_content)
            return render(request, "encyclopedia/entry.html", {"header": header, "main_content": main_content, "title" : title})
        else:
            return render(request, "encyclopedia/error.html")
    else:
        # Handle GET request
        return render(request, "encyclopedia/index.html")

    
