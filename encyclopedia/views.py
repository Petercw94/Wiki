from django.shortcuts import render
from markdown2 import markdown
from django import forms
from pprint import pprint
import random


from . import util


class SearchForm(forms.Form):
    entryField = forms.CharField(label="Search")

class NewPageForm(forms.Form):
    pageTitle = forms.CharField(label="Title")
    pageContent = forms.CharField(widget=forms.Textarea, label="Page Content (Markdown)")

class EditPageForm(forms.Form):
    pageContent = forms.CharField(widget=forms.Textarea, label="Edit Page")



def index(request):

    # create a list of all entries
    allEntries = util.list_entries()
    # search function
    # check if the search bar has been used (POST request sent) 
    if request.method == "POST":
        # assign the search value a variable
        search = SearchForm(request.POST)
        # server side validatoin
        if search.is_valid():
            # check if the search value currently has a page
            searchValue = search.cleaned_data["entryField"]
            searchResult = util.get_entry(searchValue)
            if searchResult is None:
                # return a page with entries containing the substring of searchValue
                matchedEntries = []
                for entry in allEntries:
                    if searchValue in entry:
                        matchedEntries.append(entry)
                # if the searchValue isn't in any of the entries, return an error message.
                if len(matchedEntries) == 0:
                    matchedEntries = ["No entries matched your search result."]
                # otherwise, return the searchResult.html page with the results
                context = {
                    "entries": matchedEntries,
                    "searchForm": SearchForm()
                }

                return render(request, "encyclopedia/index.html", context)
            else:
                title = searchValue
                context = {
                'title': title,
                'entry': markdown(searchResult),
                "searchForm": SearchForm(),
            }
                return render(request, "encyclopedia/entry.html", context)
            
    else:        
        return render(request, "encyclopedia/index.html", {
            "entries": allEntries,
            "searchForm": SearchForm()
        })


def entry(request, entry):
    title = entry
    try:
        entry = markdown(util.get_entry(entry))
    except TypeError:
        context = {
            'entry': f"<h1>404 Page not Found</h1><p>There is no current page for: {entry}</p>",
            'title': 'error',
            "searchForm": SearchForm(),
        }
        return render(request, "encyclopedia/entry.html", context)
    else:
        context = {
            'title': title,
            'entry': entry,
            "searchForm": SearchForm(),
        }
        return render(request, "encyclopedia/entry.html", context)

def newPage(request):
    if request.method == "POST":
        # assign the page creation a variable
        result = NewPageForm(request.POST)
        # server side validatoin
        if result.is_valid():
            # check if the page title currently has a page
            titleValue = result.cleaned_data["pageTitle"]
            pageContent = result.cleaned_data["pageContent"]
            # check if the title is part of the already created pages
            allEntries = util.list_entries()
            if titleValue in allEntries:
                context = {
                    'entry': f"<h1>Error</h1><p>There is already an entry for: {titleValue}</p>",
                    'title': 'error'
                }
                return render(request, "encyclopedia/entry.html", context)
            # if there is currently no entry for that title, create one. 
            else:
                f = open(f"./entries/{titleValue}.md", "w")
                f.write(f"{pageContent}")
                f.close()

                context = {
                    'title': titleValue,
                    'entry': markdown(util.get_entry(titleValue)),
                    'searchForm': SearchForm()
                }
                return render(request, "encyclopedia/entry.html", context)
    

    context = {
        "newPageForm": NewPageForm(),
    }
    return render(request, "encyclopedia/newPage.html", context)



def editPage(request, entry):
    # if a form was submitted:
    if request.method == "POST":
        # assign the page creation a variable
        result = EditPageForm(request.POST)
        # server side validatoin
        if result.is_valid():
            # get the pageContent
            pageContent = result.cleaned_data["pageContent"]
            # save the new page content to the appropriatefile
            f = open(f"./entries/{entry}.md", "w")
            f.write(f"{pageContent}")
            f.close()

            context = {
                'title': entry,
                'entry': markdown(util.get_entry(entry)),
                "searchForm": SearchForm(),
            }
            return render(request, "encyclopedia/entry.html", context)



    text = util.get_entry(entry)
    context = {
        "editPageForm": EditPageForm(initial={'pageContent': text}),
        "title": entry,
    }
    return render(request, "encyclopedia/editPage.html", context)


def randomPage(request):
    entries = util.list_entries()
    entry = random.choice(entries)
    context = {
        "title": entry,
        "entry": markdown(util.get_entry(entry)),
        "searchForm": SearchForm(),
    }

    return render(request, "encyclopedia/entry.html", context)