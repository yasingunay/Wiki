from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponse
from .util import get_entry, list_entries, save_entry
import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": list_entries()})


def entry(request, title):
    # If an entry is requested that does not exist,
    # the user should be presented with an error page indicating that their requested page was not found.
    if not get_entry(title):
        return render(
            request,
            "encyclopedia/error.html",
            {"message": "The page you requested was not found."},
        )
    else:
        #  If the entry does exist, the user should be presented with a page that displays the content of the entry.
        content = markdown2.markdown(get_entry(title))
        return render(
            request, "encyclopedia/entry.html", {"content": content, "title": title}
        )  # The title of the page should include the name of the entry.


def search(request):
    sub_entries = []
    if request.method == "POST":
        query = request.POST["q"]
        # If the query matches the name of an encyclopedia entry, the user should be redirected to that entry’s page.
        if query in list_entries():
            content = markdown2.markdown(get_entry(query))
            return render(
                request, "encyclopedia/entry.html", {"content": content, "title": query}
            )
        else:
            # If the query does not match the name of an encyclopedia entry,
            # the user should instead be taken to a search results page
            # that displays a list of all encyclopedia entries that have the query as a substring.
            # Clicking on any of the entry names on the search results page should take the user to that entry’s page.
            for entry in list_entries():
                if query.lower() in entry.lower():
                    sub_entries.append(entry)
            return render(
                request,
                "encyclopedia/search.html",
                {"entries": sub_entries, "query": query},
            )
    else:
        # Handle GET request
        return render(request, "encyclopedia/index.html")


def create(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create.html") 
    else:
        title = request.POST.get("title")
        description = request.POST.get("description")
        lowercase_entries = [item.lower() for item in list_entries()]
        # Check encyclopedia entry already exists case-insensetively
        if title.lower() not in lowercase_entries:
            save_entry(title, description)
            return redirect("entry", title=title)
        else:
            # If an encyclopedia entry already exists with the provided title, show error message.
            return render(
                request,
                "encyclopedia/error.html",
                {
                    "message": "The encyclopedia entry already exists with the provided title"
                },
            )


def edit(request, title):
    if request.method == "GET":
        content = get_entry(title)
        return render(
                request, "encyclopedia/edit.html", {"content": content, "title": title}
            )
    else:
        new_title = request.POST.get("new_title")
        new_description = request.POST.get("new_description")
        lowercase_entries = [item.lower() for item in list_entries()]
        # Check new_title already exists
        if new_title.lower() not in lowercase_entries or new_title.lower() == title.lower():
            title = new_title
            description = new_description
            save_entry(title, description)
            return redirect("entry", title=title)
        else:
            # If an encyclopedia entry already exists with the provided title, show error message.
            return render(
                request,
                "encyclopedia/error.html",
                {
                    "message": "The encyclopedia entry already exists with the provided title"
                },
            )