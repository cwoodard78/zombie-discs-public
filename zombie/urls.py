"""
Zombie Discs URL Configuration

This file defines the main URL routes for the project, including:
- Admin interface
- App-specific routes (users, discs, inbox)
- Static views (home, about)
- API documentation (Swagger)
- Custom error handling (404)
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from users.views import home
from django.conf.urls import handler404

# API Documentation (Swagger)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Swagger schema view for API
schema_view = get_schema_view(
    openapi.Info(
        title="Zombie Discs API",
        default_version='v1',
        description="API documentation for the Zombie Discs app",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Custom 404 Error View
def custom_404(request, exception):
    return render(request, "404.html", status=404)

handler404 = custom_404

urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),
    # DJANGO APPS
    # User app routes
    path('users/', include('users.urls')),
    # Disc app routes
    path("discs/", include("disc.urls")),
    # Inbox app routes
    path('inbox/', include('inbox.urls')),
    # PORJECT LEVEL PAGES
    # About page
    path("about/", TemplateView.as_view(template_name="about.html"), name="about"),
    # Homepage
    path('', home, name='home'),
    # Swagger API Interface
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)