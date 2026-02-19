from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),  # language switcher
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('Trafficapp.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# from django.conf.urls.i18n import i18n_patterns
# from django.contrib import admin
# from django.urls import path, include
# from django.conf import settings
# from django.conf.urls.static import static

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('Trafficapp.urls')),  # Adjust 'main' to your app's name
#     path("i18n/", include("django.conf.urls.i18n")),
# ]
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
#     urlpatterns += i18n_patterns(
#     path("", include("Trafficapp.urls")),
# )