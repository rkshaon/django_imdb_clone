from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
import requests

def index(request):
    query = request.GET.get('q')

    if query:
        url = 'http://www.omdbapi.com/?apikey=ecd537eb&s=' + query
        response = requests.get(url)
        movie_data = response.json()

        context = {
            'query': query,
            'movie_data': movie_data,
            'page_number': 1,
        }
        template = loader.get_template('search_result.html')
        return HttpResponse(template.render(context, request))

    return render(request, 'index.html')

def pagination(request, query, page_number):
    url = 'http://www.omdbapi.com/?apikey=ecd537eb&s=' + query + '&page=' + str(page_number)
    response = requests.get(url)
    movie_data = response.json()
    page_number = int(page_number) + 1
    context = {
        'query': query,
        'movie_data': movie_data,
        'page_number': page_number,
    }
    template = loader.get_template('search_result.html')
    return HttpResponse(template.render(context, request))
