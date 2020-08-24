import datetime
from datetime import date
import time

from django.http import HttpResponse
from django.shortcuts import render
import requests


# Create your views here.

def HomeView(request):
    context = None
    status = True

    while status:
        try:
            result = requests.get('https://api.covid19api.com/summary')
            json = result.json()

            globalSummary = json['Global']
            countries = json['Countries']
            active = globalSummary['TotalConfirmed'] - globalSummary['TotalRecovered'] - globalSummary['TotalDeaths']
            today = date.today()
            datetoday = today.strftime("%B %d, %Y")
            context = {"globalSummary": globalSummary, 'countries': countries, "time": datetoday, "active": active}
            time.sleep(1)
            status = False
        except:
            status = True

    return render(request, "index.html", context)


def CountryView(request, country):
    result = requests.get('https://api.covid19api.com/total/dayone/country' + '/' + str(country))
    result2 = requests.get('https://api.covid19api.com/summary')
    json2 = result2.json()
    json = result.json()
    total_case = []
    calendar = []
    dateformat = "%B %d, %Y"
    recoveries = []
    deaths = []
    for data in json:
        pass
    for data in json:
        new_date = datetime.datetime.strptime(data['Date'], "%Y-%m-%dT%H:%M:%SZ")
        calendar.append(new_date.strftime(dateformat))
    for data in json:
        total_case.append(data['Confirmed'])

    for data in json:
        recoveries.append(data['Recovered'])
    for data in json:
        deaths.append(data['Deaths'])

    total_confirmed = json[-1]['Confirmed']
    total_deaths = json[-1]['Deaths']
    total_recovered = json[-1]['Recovered']
    total_active = json[-1]['Active']

    res = dict(zip(calendar, total_case))

    region = json[-1]["Country"]

    context = {
        "country": json,
        "calendar": calendar,
        "total_case": total_case,
        "res": res,
        "Confirmed": total_confirmed,
        "Deaths": total_deaths,
        "Recovered": total_recovered,
        "Active": total_active,
        "deaths": deaths,
        "recoveries": recoveries,
        "region": region
    }
    return render(request, "country.html", context)
