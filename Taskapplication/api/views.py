from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializers import TaskSerilizer,UserSerializer
from api.models import Taskes

from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework import authentication,permissions

# Create your views here.


class TasksView(APIView):
    def get(self,request,*args,**kwargs):
        qs=Taskes.objects.all()
        desrializer=TaskSerilizer(qs,many=True)
        return Response(data=desrializer.data)
    def post(self,request,*args,**kwargs):
        serializer=TaskSerilizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

class Taskdetails(APIView):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        qs=Taskes.objects.get(id=id)
        deseializer=TaskSerilizer(qs,many=False)
        return Response(data=deseializer.data)
    def delete(self,request,*args,**kwargs):
        id=kwargs.get("id")
        Taskes.objects.get(id=id).delete()
        return Response("deleted")
    def put(self,request,*args,**kwargs):
        id=kwargs.get("id")
        obj=Taskes.objects.get(id=id)
        serializer=TaskSerilizer(data=request.data,instance=obj)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)




class TaskViewsetViews(ViewSet):
    def list(self,request,*args,**kwargs):
        qs=Taskes.objects.all()
        desrializer=TaskSerilizer(qs,many=True)
        return Response(data=desrializer.data)

    def create(self,request,*args,**kwargs):
        serializer=TaskSerilizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    def retrieve(self,request,*args,**kwargs):
        print(kwargs)
        id=kwargs.get("pk")
        qs=Taskes.objects.get(id=id)
        deseializer=TaskSerilizer(qs,many=False)
        return Response(data=deseializer.data)
    
    def update(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=Taskes.objects.get(id=id)
        serializer=TaskSerilizer(data=request.data,instance=obj)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    def destroy(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Taskes.objects.get(id=id).delete()
        return Response("deleted")




class TaskmodelViewsetView(ModelViewSet):
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    serializer_class=TaskSerilizer
    queryset=Taskes.objects.all()

    # def create(self, request, *args, **kwargs):
    #     serilizer=TaskSerilizer(data=request.data)
    #     if serilizer.is_valid():
    #         serilizer.save(user=request.user)
    #         return Response(data=serilizer.data)
    #     else:
    #         return Response(data=serilizer.errors)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def list(self,request,*args,**kwargs):
        qs=Taskes.objects.filter(user=request.user)
        print(request.user)
        desrializer=TaskSerilizer(qs,many=True)
        return Response(data=desrializer.data)

    
    @action(methods=["GET"],detail=False)
    def finished_tasks(self,request,*args,**kwargs):
        qs=Taskes.objects.filter(status=True)
        deserializer=TaskSerilizer(qs,many=True)
        return Response(data=deserializer.data)

    @action(methods=["GET"],detail=False)
    def pending_tasks(self,request,*args,**kwargs):
        qs=Taskes.objects.filter(status=False)
        deserilalizer=TaskSerilizer(qs,many=True)
        return Response(data=deserilalizer.data)
    
    @action(methods=["POST"],detail=True)
    def mark_as_done(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Taskes.objects.filter(id=id).update(status=True)
        return Response('updated')


class UserView(ModelViewSet):
    serializer_class=UserSerializer
    queryset=User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            urs=User.objects.create_user(**serializer.validated_data)
            serializer=UserSerializer(urs,many=False)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)