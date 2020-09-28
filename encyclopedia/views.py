from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from markdown2 import Markdown
from . import util
import re
import random


class NewEntryForm(forms.Form):
	title = forms.CharField()
	entry = forms.CharField(widget=forms.Textarea())

markdowner = Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, title):
	entry = util.get_entry(title)
	if(entry.startswith("#")):
		entry = re.sub(r'^\W*\w+\W*', '', entry)
	entry = markdowner.convert(entry)
	return render(request, "encyclopedia/wiki.html", {
		"entries": entry,
		"title": title 
	})

def search(request):
	keyword = request.POST["q"]
	results = []

	if (keyword.upper() in map(str.upper, util.list_entries())):
		return HttpResponseRedirect("wiki/" + keyword)
	else:
		for entry in util.list_entries():
			if (re.search(keyword, entry, re.IGNORECASE)):
				results.append(entry)
		return render(request, "encyclopedia/results.html", {"results": results})

def rando(request):
	title = random.choice(util.list_entries())
	return HttpResponseRedirect("wiki/" + title)

def create(request):
	if (request.method == "POST"):
		form = NewEntryForm(request.POST)
		if(form.is_valid()):
			title = form.cleaned_data["title"]
			entry = form.cleaned_data["entry"]
			if(title.upper() in map(str.upper, util.list_entries())):
				return HttpResponse("ERROR, AN ENTRY ALREADY EXISTS WITH THAT TITLE!")
			else:
				util.save_entry(title, entry)
				return HttpResponseRedirect("wiki/" + title)
	else:
		return render(request, "encyclopedia/create.html", {
			"form": NewEntryForm
		})

def edit(request, title):
	if (request.method == "POST"):
		entry = request.POST["e"]
		util.save_entry(title, entry)
		return HttpResponseRedirect("../wiki/" + title)
	else:
		entry = util.get_entry(title)
		if(entry.startswith("#")):
			entry = re.sub(r'^\W*\w+\W*', '', entry)
		return render(request, "encyclopedia/edit.html", {
			"entry": entry,
			"title": title
			})




