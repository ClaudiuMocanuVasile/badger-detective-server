from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import *
import sqlite3
# Create your views here.

def index(request):

    context = {}
    rows = False
    db_path = "C:\\Users\\claud\\Desktop\\product_prices.db"

    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            code = request.POST.get('link').split("/")[-2]
            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()
            rows = cursor.execute("SELECT date, price FROM prices WHERE id = ? ;", (code,)).fetchall()
            # rows = "<br>".join([str(rows[i][1]) + " RON from " + rows[i][0] + " to " + rows[i+1][0] if i < len(rows)-1 else str(rows[i][1]) + " RON as of now." for i in range(len(rows))])
    else:
        form = ClientForm()

    context = { 'client_form': form, 'rows': rows}

    return render(request, 'publicHTML/index.html', context)

