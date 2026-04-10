from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from api import views

urlpatterns = [
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterView.as_view(), name='auth_register'),
    path('', views.getRoutes),

    # Todo URLS
    path("todo/", views.TodoListView.as_view()),
    path("todo-detail/<todo_id>/", views.TodoDetailView.as_view()),
    path("todo-mark-as-completed/<todo_id>/", views.TodoMarkAsCompleted.as_view()),
]
