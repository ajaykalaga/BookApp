"""
URL configuration for BookApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Book import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('addBook', views.addBook, name='addBook'),
    path('book/<int:id>/',views.bookDetail,name='bookDetail'),
    path('recentlyAdded', views.recentlyAdded,name='recentlyAdded'),
    path('book/<int:id>/edit/',views.editBook,name='editBook'),
    path('search-suggest/', views.search_suggest, name='search_suggest'),
    path('book/<int:id>/delete/', views.deleteBook, name='deleteBook'),
    path('my-books/', views.my_books, name='myBooks'),

    # Auth
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Profiles
    path("me/", views.profile_me, name="profile_me"),
    path('u/<str:username>/', views.profile_user, name='profile_user'),
]
