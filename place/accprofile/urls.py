
from django.urls import path
from .views import *


urlpatterns = [
    # path('profile/<str:slug>', ProfileView.as_view(), name='profilepage'),
    path('', HomeNews.as_view(), name='home'),
    path('coins', Add.as_view(), name='add_coins'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('order-info/<int:pk>', OrderDetails.as_view(), name='order-details'),
    path('edit', edit, name='edit-profile'),
    path('<str:slug>', user, name='profile'),


]
