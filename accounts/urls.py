from django.urls import path

from .views import upgrade_me, UserAccountView, subscribe_to_category, unsubscribe_to_category

urlpatterns = [
    path('upgrade/', upgrade_me, name='upgrade'),
    path('user/', UserAccountView.as_view(), name='user_accounts'),
    path('subscribe/<int:pk>', subscribe_to_category, name='subscribe'),
    path('unsubscribe/<int:pk>', unsubscribe_to_category, name='unsubscribe'),

]
