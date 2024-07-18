from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
]

urlpatterns += [
    path('add_author/', views.add_author, name='add_author'),
    path('add_quote/', views.add_quote, name='add_quote'),
]

urlpatterns += [
    path('authors/', views.author_list, name='author_list'),
    path('quotes/', views.quote_list, name='quote_list'),
]


urlpatterns = [
    path('tag/<str:tag_name>/', views.tag_quotes, name='tag_quotes'),
    # Інші URL-и
]