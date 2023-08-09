from django.shortcuts import render
import requests
import json

def home(request):
    if request.method == 'POST':
        ticker = request.POST['ticker']
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
