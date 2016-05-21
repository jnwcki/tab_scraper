from django.conf.urls import url
from django.contrib import admin
from scraperapp.views import IndexView, TabListView, TabView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'(?P<url>.+html$)', TabView.as_view(), name='tab_view'),
    url(r'^tabs/(?P<url>.+)', TabListView.as_view(), name='tabs_list')
]
