from django.urls import path

path('accounts/', name='base'),

from .views import upgrade_me

urlpatterns = [
    path('upgrade/', upgrade_me, name='upgrade')
]