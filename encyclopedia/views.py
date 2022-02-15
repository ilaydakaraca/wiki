from django.shortcuts import render

from . import util
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django import forms
import markdown2
from markdown2 import Markdown
import secrets
import random



class NewPageForm(forms.Form):
    title = forms.CharField(max_length=150)
    content = forms.CharField(widget=forms.Textarea)
    edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def search(request):
    search_bar = request.GET['q']
    entries = util.list_entries()
    results = [] 

    if request.method == "GET": 
        if search_bar in entries:
            return HttpResponseRedirect(f"{search_bar}")
        
        else:
            for entry in entries:
                if search_bar in entry:
                    results.r(entry)
                    return render (request, "encyclopedia/title.html", {
                        "results": results
                    })
                else:
                    return render (request, "encyclopedia/error.html")

def title(request, title):
    markdowner = Markdown()
    entryPage = util.get_entry(title)
    if entryPage is None:
        return render(request, "encyclopedia/error.html", {
            "entryTitle": title    
        })
    else:
        return render(request, "encyclopedia/title.html", {
            "entry": markdowner.convert(entryPage),
            "entryTitle": title
        })


def random_page(request):
    entry_title = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse("title", args=(entry_title,)))

def add_page(request):
    if request.method == "POST":
        NewPage = NewPageForm(request.POST)
        if NewPage.is_valid():
                title = NewPage.cleaned_data['title']
                content = NewPage.cleaned_data['content']
                if (title in util.list_entries()):
                    return HttpResponse ("Error!! Entry already exists")
                else:    
                    util.save_entry(title, content)
                    return render(request, "encyclopedia/index.html", {
                    "entries": util.list_entries()
                    })
        else:
            return render(request, "encyclopedia/add_page.html", {
             "NewPage": NewPage
            })
    else: 
        return render(request, "encyclopedia/add_page.html", {
            "NewPage": NewPageForm()
        })

def edit(request, entry):
    if request.method == "POST":
        EditPage = NewPageForm(request.POST)
        if EditPage.is_valid():
            title = EditPage.cleaned_data['title']
            content = EditPage.cleaned_data['content']
            util.save_entry(title, content)
            return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
            })
        else:
            return render(request, "encyclopedia/edit_page.html", {
             "NewPage": EditPage
            })
    else: 
        return render(request, "encyclopedia/edit_page.html", {
            "NewPage": NewPageForm()
        })
