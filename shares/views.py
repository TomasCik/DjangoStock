from django.shortcuts import render, redirect, get_object_or_404
from .models import Stock
from django.contrib import messages
from .forms import StockForm
import requests
import json
import yfinance as yf
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64






def home(request):
    ticker = Stock.objects.all()  # gauname visus akcijų simbolius
    output = []

    for ticker_item in ticker:
        api_request = requests.get(
            f'https://api.iex.cloud/v1/data/core/quote/{ticker_item.ticker}?token=pk_e90a37e0edd44a68868fc884f83d1961')
        try:
            api = json.loads(api_request.content)
            output.append(api)
        except Exception as e:
            print(f"Error: {e}")
            return render(request, 'home.html', {'ticker': 'Invalid ticker Symbol'})

    return render(request, 'home.html', {'ticker': ticker, 'output': output})




def stock_search(request):

    if request.method == 'POST':
        ticker = request.POST['ticker_symbol']
        api_request = requests.get('https://api.iex.cloud/v1/data/core/quote/' + ticker + '?token=pk_e90a37e0edd44a68868fc884f83d1961')

        try:
            api = json.loads(api_request.content)

            if 'companyName' in api[0]:
                return render(request, 'stock_search.html', {'api': api})
            else:
                return render(request, 'stock_search.html', {'ticker': 'Invalid ticker Symbol'})
        except Exception as e:
            print(f"Error: {e}")  # Atspausdins klaidos pranešimą į konsole
            return render(request, 'stock_search.html', {'ticker': 'Invalid ticker Symbol'})

    else:
        return render(request, 'stock_search.html', {'ticker': 'Enter ticker Symbol'})

def about(request):
    return render(request, 'about.html', {})



def add_stock(request):
    if request.method == 'POST':
        form = StockForm(request.POST or None)

        # Patikriname ar toks tickeris jau egzistuoja duomenų bazėje
        if Stock.objects.filter(ticker=form.data['ticker']).exists():
            messages.error(request, 'You already have this stock')
            return redirect('add_stock')

        # Jei ne, tada tęsiame kaip įprastai
        if form.is_valid():
            # Atliekame API užklausą, kad gautume pavadinimą
            api_url = f"https://api.iex.cloud/v1/data/core/quote/{form.data['ticker']}?token=pk_e90a37e0edd44a68868fc884f83d1961"

            api_response = requests.get(api_url)
            try:
                data = api_response.json()[0]
                stock_name = data.get('companyName', 'Unknown')
            except:
                stock_name = 'Unknown'

            stock = form.save(commit=False)
            stock.companyName = stock_name
            stock.save()
            messages.success(request, 'Stock Has Been Added')
            return redirect('add_stock')
        else:
            messages.error(request, 'Invalid Ticker Symbol')
            return redirect('add_stock')

    ticker_list = Stock.objects.all()
    api_responses = []

    for stock in ticker_list:
        api_url = f'https://api.iex.cloud/v1/data/core/quote/{stock.ticker}?token=pk_e90a37e0edd44a68868fc884f83d1961'
        api_response = requests.get(api_url)
        try:
            data = api_response.json()[0]
            api_responses.append(data)
        except Exception as e:
            print(f"Error: {e}")  # Atspausdins klaidos pranešimą į konsole

    return render(request, 'add_stock.html', {'ticker': ticker_list, 'output': api_responses})


def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, 'Stock Has Been Deleted!')
    return redirect('delete_stock')


def delete_stock(request):
    ticker = Stock.objects.all()
    return render(request, 'delete_stock.html', {'ticker': ticker})


def stock_detail(request, stock_id=None):
    if stock_id:
        stock = Stock.objects.get(id=stock_id)

        # Gauname duomenis per paskutinį mėnesį
        yahoo_data = yf.Ticker(stock.ticker).history(period="5y")
        ticker_info = yf.Ticker(stock.ticker).info

        # Išskiriami reikiami duomenys iš informacijos žodyno
        stock_info = {
            'address': ticker_info['address1'],
                        'city': ticker_info['city'],
                        'state': ticker_info['state'],
                        'zip': ticker_info['zip'],
                        'country': ticker_info['country'],
                        'phone': ticker_info['phone'],
                        'website': ticker_info['website'],
                        'industry': ticker_info['industry'],
                        'priceHint': ticker_info['priceHint'],
                        'previousClose': ticker_info['previousClose'],
                        'open': ticker_info['open'],
                        'dividendRate': ticker_info['dividendRate'],
                        'dividendYield': ticker_info['dividendYield'],
                        'exDividendDate': ticker_info['exDividendDate'],
                        'payoutRatio': ticker_info['payoutRatio'],
                        'grossMargins': ticker_info['grossMargins'],
                        '52WeekChange': ticker_info['52WeekChange'],
                        'longName': ticker_info['longName']
        }

        # Verčiame DataFrame struktūrą į sąrašą žodynų
        data_list = yahoo_data.reset_index().to_dict(orient="records")
        latest_close_price = data_list[-1]['Close'] if data_list else None

        #  grafiko kūrimas naudojant seaborn
        plt.figure(figsize=(10, 5))
        sns.lineplot(x="Date", y="Close", data=yahoo_data)

        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)

        plot_url = base64.b64encode(img.getvalue()).decode('utf8')

        return render(request, 'stock_detail.html', {
            'detailed_stock': stock,
            'latest_close_price': latest_close_price,
            'yahoo_data': data_list,
            'stock_info': stock_info,
            'plot_url': plot_url
        })
    else:
        all_stocks = Stock.objects.all()
        return render(request, 'stock_detail.html', {'all_stocks': all_stocks})
