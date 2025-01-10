from django.urls import path
from . import views

urlpatterns = [
    path("submit-disc/", views.submit_disc, name="submit_disc"),
    path('disc/<int:disc_id>/', views.disc_detail, name='disc_detail'),
    path('map/', views.map_view, name='map_view'),
]