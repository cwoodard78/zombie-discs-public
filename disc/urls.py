from django.urls import path
from . import views
from .views import delete_disc
from .views import StatsAPIView
from .views import DiscListCreateAPIView, DiscDetailAPIView, RecentDiscsAPIView, DiscMapAPIView
from .views import DiscSearchView

urlpatterns = [
    path("submit-disc/", views.submit_disc, name="submit_disc"),
    path('disc/<int:disc_id>/', views.disc_detail, name='disc_detail'),
    path('disc/<int:disc_id>/edit/', views.edit_disc, name='edit_disc'),
    path('disc/<int:disc_id>/delete/', delete_disc, name='delete_disc'),
    path("my-discs/", views.user_disc_list, name="user_disc_list"),
    path('map/', views.map_view, name='map_view'),
    # path('map/select/', views.map_view, name='map_view'), UPDATE TO THIS TO BE MORE DESCRIPT
    path('map/discs/', views.disc_map_view, name='disc_map_view'),
    path('search/', DiscSearchView.as_view(), name='disc_search'),
        
    # APIs
    path('', DiscListCreateAPIView.as_view(), name='disc_list_api'),
    path('<int:pk>/', DiscDetailAPIView.as_view(), name='disc_detail_api'),
    # path('stats/', StatsAPIView.as_view(), name='stats_api'),
    path('api/stats/', StatsAPIView.as_view(), name='disc_stats_api'),
    path('recent/', RecentDiscsAPIView.as_view(), name='recent_discs_api'),
    path('api/map/', DiscMapAPIView.as_view(), name='disc_map_api'),
]