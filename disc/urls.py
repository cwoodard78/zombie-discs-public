"""
URL configuration for the Disc app.

Includes:
- User actions: submit, view, edit, delete, archive, and reactivate discs
- Matching and message functionality
- Map and search views
- REST API endpoints for frontend and external use
"""

from django.urls import path
from .views import (
    submit_disc,
    disc_detail_view,
    edit_disc,
    delete_disc,
    user_disc_list,
    user_disc_archive,
    reactivate_disc,
    mark_disc_returned,
    send_match_message,
    # disc_map_view,
    DiscSearchView,
    DiscListCreateAPIView,
    DiscDetailAPIView,
    RecentDiscsAPIView,
    StatsAPIView,
    DiscMapAPIView,
)

from . import views
from .views import StatsAPIView
from .views import DiscListCreateAPIView, DiscDetailAPIView, RecentDiscsAPIView, DiscMapAPIView
from .views import DiscSearchView

urlpatterns = [
    # Disc management (CRUD)
    path("submit-disc/", submit_disc, name="submit_disc"),
    path('disc/<int:disc_id>/', disc_detail_view, name='disc_detail'),
    path('disc/<int:disc_id>/edit/', edit_disc, name='edit_disc'),
    path('disc/<int:disc_id>/delete/', delete_disc, name='delete_disc'),
    path("my-discs/", user_disc_list, name="user_disc_list"),
    path("my-discs/archive/", user_disc_archive, name="user_disc_archive"),
    path('discs/<int:disc_id>/reactivate/', reactivate_disc, name='reactivate_disc'),
    path('disc/<int:disc_id>/returned/', mark_disc_returned, name='mark_disc_returned'),

    # Matching and messaging
    path('its-a-match/<int:disc_id>/<int:matched_disc_id>/', send_match_message, name='send_match_message'),

    # Map and search
    # Removed Google API Map for public hosting
    # path('map/discs/', disc_map_view, name='disc_map_view'),
    path('search/', DiscSearchView.as_view(), name='disc_search'),

    # API Endpoints
    path('', DiscListCreateAPIView.as_view(), name='disc_list_api'),
    path('<int:pk>/', DiscDetailAPIView.as_view(), name='disc_detail_api'),
    path('recent/', RecentDiscsAPIView.as_view(), name='recent_discs_api'),
    path('api/stats/', StatsAPIView.as_view(), name='disc_stats_api'),
    path('api/map/', DiscMapAPIView.as_view(), name='disc_map_api'),
]