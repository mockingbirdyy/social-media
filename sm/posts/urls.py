from django.urls import path
from . import views


app_name = 'posts'

urlpatterns = [
    path('', views.all_posts, name='all_posts'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', views.each_post, name='each_post'),
]