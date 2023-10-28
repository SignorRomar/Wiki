from django.shortcuts import render
import markdown

from . import util

# MARKDOWN TO HTML CONVERTER
def md_converter(title):
    content = util.get_entry(title)
    markdowner = markdown.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# RENDERS ENCYCLOPEDIA ENTRIES
def entry(request, title):
    html_content = md_converter(title)
    if html_content == None:
        return render(request, "encyclopedia/error.html")
    else:
        return render(request, "encyclopedia/entry.html",{
            "title": title,
            "content": html_content
        })

# ALLOWS USER TO USE SEARCH BAR TO FIND ENTRIES
def search(request):
    if request.method == "POST":
        entry_search = request.POST['q']
        html_content = md_converter(entry_search)
        if html_content is not None:
            return render(request, "encyclopedia/entry.html",{
            "title": entry_search,
            "content": html_content
        })

# DISPLAYS USER QUERY SUBSTRING
        else:
            all_entries = util.list_entries()
            recommendation = []
            for entry in all_entries:
                if entry_search.lower() in entry.lower():
                    recommendation.append(entry)
            return render(request,"encyclopedia/search.html",{
                "recommendation": recommendation
            } )

def new(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        titleExist = util.get_entry(title)
        if titleExist is not None:
            return render(request, "encyclopedia/error.html",{
                "message": "Entry page already exists."
            })
        else: 
            util.save_entry(title, content)
            html_content = md_converter(title)
            return render(request, "encyclopedia/entry.html",{
                "title": title,
                "content": html_content
            })