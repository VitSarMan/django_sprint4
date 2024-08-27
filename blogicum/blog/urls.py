from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path(
        'category/<slug:category_slug>/',
        views.category_posts, name='category_posts'
    ),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('create/', views.PostCreateView.as_view(), name='create_post'),
    path('', views.index, name='index'),
    path('profile/<str:username>/', views.UserDetailView.as_view(), name='profile'),
    

]

# urlpatterns = [
#     #path('', views.birthday, name='create'),
#     # Декорируем вызов метода as_view(), без синтаксического сахара:
#     path('create/', login_required(views.BirthdayCreateView.as_view()), name='create'),
#     #path('list/', views.birthday_list, name='list'),
#     path('list/', views.BirthdayListView.as_view(), name='list'),
#     path('<int:pk>/', views.BirthdayDetailView.as_view(), name='detail'),
#     #path('<int:pk>/edit/', views.birthday, name='edit'),
#     path('<int:pk>/edit/', views.BirthdayUpdateView.as_view(), name='edit'),
#     #path('<int:pk>/delete/', views.delete_birthday, name='delete'),
#     path('<int:pk>/delete/', views.BirthdayDeleteView.as_view(), name='delete'),
#     path('login_only/', views.simple_view),
#     path('<int:pk>/comment/', views.add_comment, name='add_comment'),
# ]