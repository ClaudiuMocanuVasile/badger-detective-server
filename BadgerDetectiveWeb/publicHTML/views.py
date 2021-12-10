from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import *
import sqlite3
# Create your views here.

def index(request):

    context = {}

    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            code = request.POST.get('link').split("/")[-2]
            connection = sqlite3.connect("product_prices.db")
            cursor = connection.cursor()
            link = cursor.execute("SELECT date, price FROM prices WHERE id = ? ;", (code,)).fetchall()
    else:
        form = ClientForm()
        link = ""

    context = { 'client_form': form, 'link': link}

    return render(request, 'publicHTML/index.html', context)
