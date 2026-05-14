
from django.contrib import admin
from django.urls import include, path


api_patterns = [
    path("", include("core.apps.users.urls")),
    path("", include("core.apps.workers.urls")),
    path("", include("core.apps.orders.urls")),
    path("", include("core.apps.notifications.urls")),
    path("", include("core.apps.payments.urls")),
    path("", include("core.apps.ratings.urls")),
    path("", include("core.apps.favorites.urls")),
]
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_patterns)),
]
