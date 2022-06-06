from django.urls import path
from . import views

app_name = "articles"
urlpatterns = [
    path('', views.list, name="list"),
    path('create/', views.create, name="create"),
    path('<int:pk>/', views.detail, name="detail"),
    path('<int:pk>/delete', views.delete, name="delete"),
    path('<int:pk>/update', views.update, name="update"),
    path('<int:pk>/comment_create', views.comment_create, name="comment_create"),
    path('<int:article_pk>/comment_delete/<int:comment_pk>/delete', views.comment_delete, name="comment_delete"),
]
