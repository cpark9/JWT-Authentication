# class TodoMarkAsCompleted(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = TodoSerializer

#     def get_object(self):
#         user_id = self.kwargs['user_id']
#         todo_id = self.kwargs['todo_id']

#         user = User.objects.get(id=user_id)
#         todo = Todo.objects.get(id=todo_id, user=user)

#         todo.completed = True
#         todo.save()

#         return todo  


# class TodoListView(generics.ListCreateAPIView):
#     queryset = Todo.objects.all()
#     serializer_class = TodoSerializer

#     def get_queryset(self):
#         user_id = self.kwargs['user_id']
#         user = User.objects.get(id=user_id)

#         todo = Todo.objects.filter(user=user) 
#         return todo

# class TodoDetailView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = TodoSerializer

#     def get_object(self):
#         user_id = self.kwargs['user_id']
#         todo_id = self.kwargs['todo_id']

#         user = User.objects.get(id=user_id)
#         todo = Todo.objects.get(id=todo_id, user=user)

#         return todo
