
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path


api_patterns = [
    path("", include("apps.users.urls")),
    path("", include("apps.workers.urls")),
    path("", include("apps.orders.urls")), 
    path("", include("apps.notifications.urls")),
    path("", include("apps.payments.urls")),
    path("", include("apps.ratings.urls")),
    path("", include("apps.favorites.urls")),

]
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_patterns)),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
