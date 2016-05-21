import requests
from django.views.generic import TemplateView
from bs4 import BeautifulSoup
from django.shortcuts import render


class IndexView(TemplateView):
    template_name = 'index.html'

    def post(self, request):
        searched_song = self.request.POST.get('song_search_string')
        searched_band = self.request.POST.get('band_search_string')
        scraped_content = requests.get("http://www.guitartabs.cc/search.php?tabtype=any&band={}&song={}".format(
                                       searched_band,
                                       searched_song
                                       )).content
        bb_obj = BeautifulSoup(scraped_content, 'html.parser')
        results_list = str(bb_obj.find_all(class_='tabslist fs-12'))
        return render(request, 'list.html', {"scraped_content": results_list})


class TabListView(TemplateView):
    template_name = 'list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        scraped_content = requests.get("http://www.guitartabs.cc/tabs/{}".format(
                                       kwargs['url'],
                                       )).content
        bb_obj = BeautifulSoup(scraped_content, 'html.parser')
        results_list = bb_obj.find_all(class_='tabslist')
        context['scraped_content'] = results_list
        return context


class TabView(TemplateView):
    template_name = 'tab.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        scraped_content = requests.get("http://guitartabs.cc/{}".format(
            kwargs['url'])).content
        bb_obj = BeautifulSoup(scraped_content, 'html.parser')
        results_list = [result.prettify() for result in bb_obj.find_all('pre')]
        context['scraped_content'] = results_list
        return context
