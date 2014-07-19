from django.conf.urls import patterns, include, url
from core.views import HomeView, PollingAPIView
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'blockduino.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/poll/', PollingAPIView.as_view(), name='polling')
)
