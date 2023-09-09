from django.shortcuts import render, redirect
from django import forms
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
    sub_entries= []
    if request.method == "POST":
        query = request.POST["q"]
        # If the query matches the name of an encyclopedia entry, the user should be redirected to that entry’s page.
        if query in list_entries():
            html_content = markdown_to_html(query)
            header, main_content = separate_markdown_content(html_content)
            return render(request, "encyclopedia/entry.html", {"header": header, "main_content": main_content, "title" : query})
        else:
            # If the query does not match the name of an encyclopedia entry, 
            # the user should instead be taken to a search results page 
            # that displays a list of all encyclopedia entries that have the query as a substring. 
            # Clicking on any of the entry names on the search results page should take the user to that entry’s page.
            for entry in list_entries():
                if query.lower()in entry.lower():
                    sub_entries.append(entry)
            return render(request, "encyclopedia/search.html", {"entries": sub_entries, "query" : query})
            
           
    else:
        # Handle GET request
        return render(request, "encyclopedia/index.html")

    
