from django.shortcuts import render
from encyclopedia import util
import re


def index(request):
	print(util.list_entries());
	return render(request, "encyclopedia/index.html",{ "entries": util.list_entries()})

def info(request, title):
	return render(request, "wiki/info.html",{ "entries":util.get_entry(title)})