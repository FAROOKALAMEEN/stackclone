from django.urls import path
from taskweb import views

urlpatterns=[
    path('signup/',views.SignUpView.as_view(),name="reg"),
    path('',views.SignInView.as_view(),name="signin"),
    path('home/',views.IndexView.as_view(),name="homes"),
    path('tasks/add/',views.TaskCreateView.as_view(),name="task-add"),
    path('tasks/all/',views.TaskListView.as_view(),name="task-lists"),
    path('tasks/details/<int:id>/',views.TaskDetailView.as_view(),name="todo-detail"),
    path('task/remove/<int:id>/',views.TaskDeleteView.as_view(),name="task-delete"),
    path('task/<int:id>/change/',views.TaskEditView.as_view(),name="task-edit"),
    path('signout/',views.LogOutView.as_view(),name='signout')

]