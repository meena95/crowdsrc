from django.conf.urls import include,url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #url(r'^',admin.site.urls),
    url(r'^admin/', admin.site.urls),
    url(r'^crowdsrc/', include('crowdsrc.urls')),
    url(r'^', include('crowdsrc.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)