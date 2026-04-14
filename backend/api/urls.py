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

    # Chat/Text Messaging Functionality
    path("my-messages/", views.MyInbox.as_view()),
    path("get-messages/<reciever_id>/", views.GetMessages.as_view()),
    path("send-messages/", views.SendMessages.as_view()),

    # Get profile
    path("profile/<int:pk>/", views.ProfileDetail.as_view()),
    path("search/<username>/", views.SearchUser.as_view()),
]
