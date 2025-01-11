from django.urls import path
from . import views
from .views import delete_disc

urlpatterns = [
    path("submit-disc/", views.submit_disc, name="submit_disc"),
    path('disc/<int:disc_id>/', views.disc_detail, name='disc_detail'),
    path('disc/<int:disc_id>/edit/', views.edit_disc, name='edit_disc'),
    path('disc/<int:disc_id>/delete/', delete_disc, name='delete_disc'),
    path("my-discs/", views.user_disc_list, name="user_disc_list"),
    path('map/', views.map_view, name='map_view'),
]