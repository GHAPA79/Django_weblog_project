from django.urls import path

from .views import *

urlpatterns = [
    path('', PostsListView.as_view(), name='posts_list'),
    path('<int:pk>/', post_detail_view, name='post_details'),
    path('addpost', PostCreateView.as_view(), name='create_post'),
    path('<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='delete_post'),
]
