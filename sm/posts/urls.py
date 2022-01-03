from django.urls import path
from . import views


app_name = 'posts'

urlpatterns = [
    path('', views.all_posts, name='all_posts'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', views.each_post, name='each_post'),
    path('Add_post/<int:user_id>/', views.add_post, name='add_post'),
    path('Delete_post/<int:user_id>/<int:post_id>/', views.delete_post, name='delete_post'),
    path('Edit_post/<int:user_id>/<int:post_id>/', views.edit_post, name='edit_post'),
    path('Add_reply/<int:post_id>/<int:comment_id>/', views.add_reply, name='add_reply'),
]