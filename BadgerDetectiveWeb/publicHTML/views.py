from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import *
# Create your views here.

def index(request):

    context = {}

    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            link = request.POST.get('link').split("/")[-2]

    else:
        form = ClientForm()

    context = { 'client_form': form, 'link': link}

    return render(request, 'publicHTML/index.html', context)