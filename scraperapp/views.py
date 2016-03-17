import requests
from django.views.generic import TemplateView, View
from bs4 import BeautifulSoup

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            searched_song = self.request.GET.get('song_search_string')
            searched_band = self.request.GET.get('band_search_string')
            scraped_content = requests.get("http://www.guitartabs.cc/search.php?tabtype=any&band={}&song={}".format(
                                           searched_band,
                                           searched_song
                                           )).content
            # context['scraped_content'] = scraped_content
            bb_obj = BeautifulSoup(scraped_content, 'html.parser')
            results_list = bb_obj.find_all(class_='tabslist fs-12')
            print(results_list)
            context['scraped_content'] = results_list
        return context


class TabView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print("http://www.guitartabs.cc/tabs/{}".format(kwargs['url']))
        scraped_content = requests.get("http://www.guitartabs.cc/{}".format(
                                       kwargs['url'],
                                       )).content
        context['scraped_content'] = scraped_content
        bb_obj = BeautifulSoup(scraped_content, 'html.parser')
        results_list = bb_obj.find_all(class_='tabslist fs-12')
        print(results_list)
        # context['scraped_content'] = results_list
        return context
