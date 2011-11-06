from django.conf.urls.defaults import patterns, include, url
import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^scan/?$', 'audio.views.scan_media'),
    url(r'^songs/?$', 'audio.views.list_songs'),
    url(r'^songs/delete/?$', 'audio.views.delete_songs'),
    url(r'^songs/(\d+)/play/?$', 'audio.views.play_song'),
    url(r'^songs/(\d+)/stream/?$', 'audio.views.stream_song'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, "show_indexes": True}),
)
