from django.shortcuts import render, redirect
import requests
import json
from .models import Stock
from django.contrib import messages
from .forms import StockForm
from django.http import HttpResponseBadRequest


def home(request):
    if request.method == 'POST':
        ticker = request.POST['ticker_symbol']
        api_request = requests.get('https://api.iex.cloud/v1/data/core/quote/' + ticker + '?token=pk_e90a37e0edd44a68868fc884f83d1961')

        try:
            api = json.loads(api_request.content)
            if 'companyName' in api[0]:
                return render(request, 'home.html', {'api': api})
            else:
                return render(request, 'home.html', {'ticker': 'Invalid ticker Symbol'})
        except Exception as e:
            print(f"Error: {e}")  # Atspausdins klaidos pranešimą į konsole
            return render(request, 'home.html', {'ticker': 'Invalid ticker Symbol'})

    else:
        return render(request, 'home.html', {'ticker': 'Enter ticker Symbol'})

def about(request):
    return render(request, 'about.html', {})


def add_stock(request):
    if request.method == 'POST':
        form = StockForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Stock Has Been Added')
        else:
            messages.error(request, 'Invalid Ticker Symbol')
    else:
        form = StockForm()  # Sukurkite formą, jei užklausa nėra POST

    ticker = Stock.objects.all()
    context = {'ticker': ticker, 'form': form}  # Pridėkite 'form' į kontekstą
    return render(request, 'add_stock.html', context)


def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, ('Stock Has Been Deleted!'))
    return redirect(add_stock)

