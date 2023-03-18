from django.shortcuts import render

from api.serializers import UserSerializer,ProfileSerializer,QuestionSerializer,AnswerSerializer
from rest_framework.response import Response


from rest_framework.viewsets import ViewSet,ModelViewSet,GenericViewSet
from django.contrib.auth.models import User
from stackweb.models import UserProfile,Questions,Answers

from rest_framework.mixins import CreateModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework import authentication,permissions
from rest_framework.decorators import action
from rest_framework import serializers

# create
class UsersView(GenericViewSet,CreateModelMixin):
    serializer_class=UserSerializer
    queryset=User.objects.all()
    
# create,detail,edit,delete 
class ProfileView(ModelViewSet):
    serializer_class=ProfileSerializer
    queryset=UserProfile.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
# WE INHERIT ModelViewSet THEN CreateModelMixin SO WE CAN REDUCE THE CODE SIZE BY OVERRIDING DEF CREATE(THAYE ULLATH)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    
    # FOR CREATING USER
    # def create(self, request, *args, **kwargs):
    #     serializer=ProfileSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save(user=request.user)
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(data=serializer.errors)
         
        
        
    # def list(self, request, *args, **kwargs):
    #     qs=UserProfile.objects.get(user=request.user)
    #     serializer=ProfileSerializer(qs,many=False)
    #     return Response(data=serializer.data)
    
    # OVER RIDE ABOVE LIST FUNCTION AND REDUCE CODE SIZE
    
    def get_queryset(self):
         return UserProfile.objects.filter(user=self.request.user)
     
     

    def destroy(self,request,*args,**kwargs): 
        # to get the profile with that id
        prof=self.get_object() 
        if prof.user  != request.user:
            #  profile user and token send user aanenkil block
            raise serializers.ValidationError("not allow to perform")
        else:
            return super().destroy(request,*args,**kwargs)
        
             
         
    # def create(self,request,*args,**kwargs):
    #     serializer=UserSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(data=serializer.errors)
        
         
# questiion list cheyyan
class QuestionsView(ModelViewSet):
    serializer_class=QuestionSerializer
    queryset=Questions.objects.all()
# unauthorized user avoid aakanam token sent cheytha usern maathram questionte mele activity cheyaan pattoolu
    # authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

# to add question we need to send user details for adding question so we need to override create method 

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
        
    @action(methods=["post"],detail=True)    
    def add_answer(self,request,*args,**kwargs):
        serializer=AnswerSerializer(data=request.data)
        id=kwargs.get("pk")
        quest=Questions.objects.get(id=id)
        user=request.user
        if serializer.is_valid():
            serializer.save(user=user,question=quest)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
# ITHINTE PAKARAM QUESTION MODEL KODKUKAA
    # def get_queryset(self):
    #     return Questions.objects.all().order_by("-created_date")
    
    
class AnswersView(ModelViewSet):
    serializer_class=AnswerSerializer
    queryset=Answers.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        raise serializers.ValidationError("method not allowed")
    
    
    @action(methods=["post"],detail=True)
    def add_upvote(self,request,*args,**kwargs):
        answer=self.get_object()
        answer.upvote.add(request.user)
        answer.save()
        return Response(data="upvoted")
    
    @action(methods=["post"],detail=True)
    def down_vote(self,request,*args,**kwargs):
        answer=self.get_object()
        answer.upvote.remove(request.user)
        answer.save()
        return Response(data="upvote removed")
    
    
    
    