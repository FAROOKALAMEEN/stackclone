from django.shortcuts import render,redirect
from django.views.generic import View
from taskweb.forms import UserForm,LoginForm,TasksForm,TaskEditForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from api.models import Taskes
from django.utils.decorators import method_decorator
from django.contrib import messages


# Create your views here.
def created_decorator(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect('signin')
        else:
            return fn(request,*args,**kwargs)
    return wrapper

class SignUpView(View):
    
    def get(self,request,*args,**kwargs):
        form=UserForm()
        return render(request,"register.html",{"forms":form})

    def post(self,request,*args,**kwargs):
        form=UserForm(request.POST)
        if form.is_valid():
            form.save()
            User.objects.create_user(**form.cleaned_data)
            messages.success(request,"Account has been Succesfully Created")
            return redirect("signinname")
        else:
            messages.error(request,("Faild to Register"))
            return render(request,"register.html",{"forms":form})


class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"login.html",{"forms":form})
    
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                return redirect("homes")
            else:
                return render(request,"login.html",{"forms":form})

@method_decorator(created_decorator,name='dispatch')
class IndexView(View):
    def get(self,request,*args,**kwargs):
        return render(request,"index.html")

@method_decorator(created_decorator,name='dispatch')
class TaskCreateView(View):
    def get(self,request,*args,**kwargs):
        form=TasksForm()
        return render(request,"task-add.html",{"forms":form})
    
    def post(self,request,*args,**kwargs):
        form=TasksForm(request.POST)
        if form.is_valid():
            form.instance.user=request.user
            form.save()
            messages.success(request,"Tasks has ben created successfully")
            return redirect('task-lists')
        else:
            messages.error(request,"faild to add Task")
            return render(request,"task-add.html",{"forms":form})

@method_decorator(created_decorator,name='dispatch')
class TaskListView(View):
    def get(self,request,*args,**kwargs):
        qs=Taskes.objects.filter(user=request.user).order_by("-created_date")
        return render(request,"task-list.html",{"tasks":qs})

@method_decorator(created_decorator,name='dispatch')
class TaskDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        qs=Taskes.objects.get(id=id)
        return render(request,"task-detail.html",{"task":qs})

@method_decorator(created_decorator,name='dispatch')
class TaskDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        Taskes.objects.filter(id=id).delete()
        messages.warning(request,"task deleted")
        return redirect("task-lists")

@method_decorator(created_decorator,name='dispatch')
class TaskEditView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        obj=Taskes.objects.get(id=id)
        form=TaskEditForm(instance=obj)
        return render(request,"task-edit.html",{"form":form})

    def post(self,request,*args,**kwargs):
        id=kwargs.get("id")
        obj=Taskes.objects.get(id=id)
        form=TaskEditForm(request.POST,instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request,"Tasks has been succefully Updated")
            return redirect("task-lists")
        else:
            messages.error(request,"Faild to Update")
            return render(request,"task-edit.html",{"form":form})

@method_decorator(created_decorator,name='dispatch')
class LogOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect('signin')