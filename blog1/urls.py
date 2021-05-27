from django.urls import path, include
from .views import dashboard, home, login, register, logout, addArticle, viewArticle, editArticle, deleteArticle

urlpatterns = [
    path('', home, name='home_page'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('dashboard/<slug:username>', dashboard, name='dashboard'),
    path('dashboard/<slug:username>/', dashboard, name='dashboard'),
    path('dashboard/<slug:username>/add', addArticle, name='addArticle'),
    path('dashboard/<slug:username>/<slug:slugtitle>', viewArticle, name='viewArticle'),
    path('dashboard/<slug:username>/<slug:slugtitle>/edit', editArticle, name='viewArticle'),
    path('dashboard/<slug:username>/<slug:slugtitle>/delete', deleteArticle, name='viewArticle'),
    path('logout/', logout, name='logout'),
]