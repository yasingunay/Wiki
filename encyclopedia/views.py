from django.shortcuts import render
from django.http import HttpResponse
from .util import get_entry

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
        print(type(get_entry(title)))
        return render(request, "encyclopedia/error.html")
    
        
