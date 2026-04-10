from django.shortcuts import render

from api.models import User, Profile, Todo
from api.serializer import RegisterSerializer, UserSerializer, MyTokenObtainPairSerializer, TodoSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer 

@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token/',
        '/api/register/',
        '/api/token/refresh/'
    ]
    return Response(routes)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def testEndPoint(request):
    if request.method == 'GET':
        data = f"Congratulation {request.user}, your API just responded to GET request"
        return Response({'response': data}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        text = f"Hello!!! {request.user}"
        data = f'Congratulation your API just responded to POST request with text: {text}'
        return Response({'response': data}, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid request method.'}, status=status.HTTP_400_BAD_REQUEST) 



# TodoListView에서 로그인한 사용자 본인의 데이터만 반환하도록 수정하여 보안 강화(get_queryset 메서드 수정)   
class TodoListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    def get_queryset(self):
        # 로그인한 사용자 본인의 데이터만 반환하여 보안 강화
        return Todo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # 할 일 생성 시 현재 로그인한 유저를 자동으로 할당
        serializer.save(user=self.request.user)

# # TodoDetailView에서 로그인한 사용자 본인의 데이터만 반환하도록 수정하여 보안 강화(get_object 메서드 수정)
class TodoDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TodoSerializer

    def get_object(self):
        todo_id = self.kwargs.get('todo_id')
        return Todo.objects.get(id=todo_id, user=self.request.user)

# TodoMarkAsCompleted에서 로그인한 사용자 본인의 데이터만 반환하도록 수정하여 보안 강화(get_object 메서드 수정)
class TodoMarkAsCompleted(generics.UpdateAPIView): # 단순 업데이트이므로 UpdateAPIView 권장
    permission_classes = [IsAuthenticated]
    serializer_class = TodoSerializer

    def get_object(self):
        todo_id = self.kwargs.get('todo_id')
        todo = Todo.objects.get(id=todo_id, user=self.request.user)
        todo.completed = True
        todo.save()
        return todo
