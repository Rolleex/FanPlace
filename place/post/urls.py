from django.urls import path
from .views import *

urlpatterns = [
    path('add-news', NewPost.as_view(), name='create_post'),
    path('post/<str:slug>', postview, name='post'),
    path('pay/<str:slug>', pay, name='pay'),
    path('search', Search.as_view(), name='search'),
    path('feed', feed, name='feed')

]
