from django.shortcuts import render
from django.db.models import Q, OuterRef, Subquery

from api.models import User, Profile, Todo, ChatMessage
from api.serializer import RegisterSerializer, UserSerializer, MyTokenObtainPairSerializer, TodoSerializer, MessageSerializer, ProfileSerializer

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
    
# Chat APp
class MyInbox(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id

        messages = ChatMessage.objects.filter(
            id__in =  Subquery(
                User.objects.filter(
                    Q(sender__reciever=user_id) |
                    Q(reciever__sender=user_id)
                ).distinct().annotate(
                    last_msg=Subquery(
                        ChatMessage.objects.filter(
                            Q(sender=OuterRef('id'),reciever=user_id) |
                            Q(reciever=OuterRef('id'),sender=user_id)
                        ).order_by('-id')[:1].values_list('id',flat=True) 
                    )
                ).values_list('last_msg', flat=True).order_by("-id")
            )
        ).order_by("-id")
            
        return messages
    
class GetMessages(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # URL에서 상대방 ID를 가져옵니다.
        reciever_id = self.kwargs['reciever_id']
        # 발신자는 항상 현재 로그인한 유저로 고정하여 보안을 강화합니다.
        user_id = self.request.user.id

        # Q 객체를 사용하여 (나 -> 상대방) 또는 (상대방 -> 나)인 메시지만 정확히 필터링합니다.
        messages = ChatMessage.objects.filter(
            Q(sender=user_id, reciever=reciever_id) | 
            Q(sender=reciever_id, reciever=user_id)
        ).order_by("date") # 대화 흐름을 위해 과거 메시지부터 정렬
        
        return messages


class SendMessages(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # 메시지 저장 시 sender와 user를 현재 로그인한 유저로 강제 지정합니다.
        # 이를 통해 다른 사람의 ID로 메시지를 보내는 사칭을 방지합니다.
        serializer.save(sender=self.request.user, user=self.request.user)


class ProfileDetail(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]  

    def get_object(self):
        # URL에 어떤 숫자가 들어오든 상관없이, 현재 로그인한 유저(request.user)와 연결된 프로필(profile)만 딱 집어서 반환합니다.
        # 이 방식을 통해 자신의 프로필만 조회/수정할 수 있도록 강제합니다.
        return self.request.user.profile


class SearchUser(generics.ListAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]  

    def get_queryset(self):
        username = self.kwargs['username']
        logged_in_user = self.request.user

        # 괄호를 사용하여 (검색 조건들) AND (내가 아님) 로직을 명확히 합니다.
        queryset = Profile.objects.filter(
            (Q(user__username__icontains=username) | 
             Q(full_name__icontains=username) | 
             Q(user__email__icontains=username)) & 
            ~Q(user=logged_in_user)
        )
        return queryset
