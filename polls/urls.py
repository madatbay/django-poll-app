from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name = 'index'),
    path('<int:pk>/', views.DetailView.as_view(), name = 'detail'),
    path('<int:question_id>/results/', views.results, name = 'results'),
    path('<int:question_id>/vote/', views.vote, name = 'vote'),
    path('login/', views.loginUser, name = 'login'),
    path('logout/', views.logoutUser, name = 'logout'),
    path('register/', views.register, name = 'register'),
    path('create/', views.createPoll, name = 'create'),

]