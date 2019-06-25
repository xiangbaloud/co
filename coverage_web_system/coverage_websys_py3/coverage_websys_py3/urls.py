from django.conf.urls import include, url
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib import admin
from filebrowser.sites import site
from filebrowser.sites import FileBrowserSite
from django.core.files.storage import DefaultStorage

# django_version=="2.1"
urlpatterns = [
    path('test-history/', site.urls),
    path('admin/', admin.site.urls),
    path('cws/', include('coverage_websys_func.urls')),
    path('', RedirectView.as_view(url='/cws', permanent=True)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# config admin page
admin.site.site_header = 'Coverage - Test Web System Admin'
admin.site.index_title = 'coverage - test web system '
admin.site.site_title = 'administration'

#
c_site = FileBrowserSite(name='FB', app_name='filebrowser', storage=DefaultStorage())