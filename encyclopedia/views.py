from django.shortcuts import render
from django.http import HttpResponse
from .util import markdown_to_html
from .util import get_entry, separate_markdown_content

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
        html_content = markdown_to_html(title)
        header, main_content = separate_markdown_content(html_content)
        print(header)
        return render(request, "encyclopedia/entry.html", {"header": header, "main_content": main_content, "title" : title})
    
        
