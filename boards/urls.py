from django.urls import path

from . import views

app_name = 'boards'

urlpatterns = [
    path('', views.BoardListView.as_view(), name='home'),
    path('boards/<int:pk>/', views.TopicListView.as_view(), name='board'),
    path('boards/<int:pk>/new/', views.new_topic_view, name='new_topic'),
    path('boards/<int:pk>/topics/<int:topic_pk>/', views.PostListView.as_view(), name='topic_posts'),
    path('boards/<int:pk>/topics/<int:topic_pk>/reply/', views.reply_view, name='reply'),
    path('boards/<int:pk>/topics/<int:topic_pk>/posts/<int:post_pk>/edit/',
         views.PostUpdateView.as_view(), name='edit'),
    path('account/', views.UserUpdateView.as_view(), name='account')
]
