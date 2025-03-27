from django.urls import path
from . import views

urlpatterns = [
    path('inbox/<int:receiver_id>/<int:disc_id>/', views.send_message, name='send_message'),
    path('inbox/<int:receiver_id>/', views.send_message, name='send_message'),
    path('inbox/', views.inbox_view, name='inbox'),
    path('inbox/delete/<int:message_id>/', views.delete_message, name='delete_message'),

    # DEBUG
    path('inbox/test/', views.test_view, name='test_view'),
]
