from django.shortcuts import render, redirect
from . import util
import markdown2, re, random

wlist = util.list_entries()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": wlist
    })

def wiki(request, title):
    listitem = util.get_entry(title)
    if listitem != None:
        return render(request, "encyclopedia/item.html", {
            "title": title,
            "listitem": markdown2.markdown(listitem)
        })
    else:
        return render(request, "encyclopedia/error.html", {
            'error_message': "Sorry, The page doesn't exist."
            })

def edit(request, title):
    if request.method == 'POST':
        listitem2 = request.POST.get('changed_item')
        util.save_entry(title, listitem2)
        return redirect(wiki, title=title)

    else:
        listitem2 = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            'title': title,
            'listitem': listitem2
            })

def search(request):
    if request.method == 'POST':
        term = request.POST['q']
        searchlist = []

        for listitem in wlist:

            if re.search(term.lower(), listitem.lower()):  # case in sensitive
                searchlist.append(listitem)
        if len(searchlist) == 0:  # searchlist is empty
            return render(request, "encyclopedia/error.html", {
                'error_message': f'No results found for \'{term}\' '
            })

    return render(request, "encyclopedia/search.html", {
        'entries': searchlist
    })

def new(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        print(f"{content}")
        util.save_entry(title, content)
        return redirect(wiki, title=title)

    return render(request, "encyclopedia/new.html")

def random2(request):
    title = random.choice(wlist)
    return redirect(wiki, title=title)