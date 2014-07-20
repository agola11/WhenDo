from django.conf.urls import patterns, include, url
from core.views import HomeView, PollingAPIView, new_module, poll_from_serial, compiler, delete_pickle
from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'blockduino.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^newmod/$', new_module, name='new_module'),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^delete_pickle/',delete_pickle, name='delete_pickle'),
    url(r'^api/poll/', PollingAPIView.as_view(), name='polling'),
    url(r'^directives/when/', TemplateView.as_view(template_name='when.html'), name='when'),
    url(r'^directives/do/', TemplateView.as_view(template_name='do.html'), name='do'),
    url(r'^compile/', compiler, name='compiler'),
    url(r'^poll_new/', poll_from_serial, name='poll'),
    url(r'^directives/display_table/', TemplateView.as_view(template_name='display_table.html'), name='table')
)
