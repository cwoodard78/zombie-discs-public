"""
URL configuration for zombie project.
Defines routes for admin, apps, static files, and API documentation.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from users.views import home

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
    # Update API permission to require authentication
    # permission_classes=(permissions.IsAuthenticated,),
)

urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),
    # User app
    path('users/', include('users.urls')),
    # Disc app
    path("discs/", include("disc.urls")),
    # About page
    path("about/", TemplateView.as_view(template_name="about.html"), name="about"),
    # Homepage
    path('', home, name='home'),
    # Inbox
    path('inbox/', include('inbox.urls')),
    # Swagger API Interface
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # Hamburger troubleshooting
    path('burger-test/', TemplateView.as_view(template_name='burger_test.html'), name='burger_test'),

]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)