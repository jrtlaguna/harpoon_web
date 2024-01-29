from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("", include("core.urls")),
    path("", include("authentication.urls")),
    path("admin/", include("admins.urls")),
    path("guest/", include("guests.urls")),
    path("charter/", include("charter.urls")),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("vessels/", include("vessels.urls")),
    path("preferences/", include("preferences.urls")),
    path("django-admin/", admin.site.urls),
]

# handler404 = "authentication.views.handler404"
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
