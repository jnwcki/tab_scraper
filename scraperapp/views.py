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
        results_list = [result.prettify() for result in bb_obj.find_all(class_='tabslist')]

        table_results_list = BeautifulSoup(results_list[0], 'html.parser')
        # print(table_results_list.prettify())
        # for tag in table_results_list.select('table'):
        #     tag['class'] = 'table'
        # print(table_results_list.prettify())
        return render(request, 'list.html', {"scraped_content": table_results_list.prettify()})


class TabListView(TemplateView):
    template_name = 'list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        scraped_content = requests.get("http://www.guitartabs.cc/tabs/{}".format(
                                       kwargs['url'],
                                       )).content
        bb_obj = BeautifulSoup(scraped_content, 'html.parser')
        results_list = bb_obj.find_all(class_='tabslist')
        print(results_list)
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

        tab_pane = BeautifulSoup(results_list[1], 'html.parser')
        tab_pane.span.decompose()
        for tag in tab_pane.select('a'):
            tag.unwrap()
        results_list[1] = tab_pane.prettify()
        context['scraped_content'] = results_list
        return context
