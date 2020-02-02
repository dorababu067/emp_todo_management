from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout
from .firebase_config import (fire_auth, fire_db, 
            create_task, get_tasks, get_task_data,
            check_user_login_or_not,
            get_task_data_update, create_emp)
from django.contrib.auth.decorators import login_required
from . forms import TaskForm
from django.contrib import messages


# Create your views here.
def index(request):
    # print(request.session.session_key)
    try:
        uid = request.session['uid']
        username = fire_db.child("users").child(uid).child("profile").child("username").get().val()
        return render(request, 'home.html',{"username": username})
    except:
        return render(request, 'home.html')

def emp_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 != password2 :
            messages.warning(request, 'Please check your Password is mismatch')
        else:
            create_emp(username = username, email= email, password = password1)
            messages.success(request, 'Your accout is created succesfully')
    return render(request, 'register.html')


def emp_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = fire_auth.sign_in_with_email_and_password(email, password)
            request.session['uid'] = str(user['localId'])
            request.session['user'] = { "login" : True }
            return redirect(emp_task)
        except:
            messages.warning(request, "Please check your email and password")
            return render(request, 'login.html')
    user = check_user_login_or_not()
    if user.get("login"):
        uid = request.session['uid']
        tasks = get_tasks(uid)
        form = TaskForm()
        return render(request, 'emp-todo.html',{"username": user.usename, "tasks":tasks, "form":form})
    else:
        return render(request, 'login.html')


def emp_logout(request):
    logout(request)
    return redirect(emp_login) 

def emp_task(request):
    form = TaskForm()
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        spent_time = request.POST['spent_time']
        uid = request.session['uid']
        create_task(uid = uid, title = title, description = description, spent_time = spent_time)
        messages.success(request, "Your task created successfully")
        tasks = get_tasks(uid)
        context = {
            "form":form,
            "tasks": tasks
        }
        return render(request, 'emp-todo.html', context)
    uid = request.session['uid']
    tasks = get_tasks(uid)
    username = fire_db.child("users").child(uid).child("profile").child("username").get().val()
    return render(request, 'emp-todo.html', {"form":form, "tasks": tasks, "username": username})

def update_task(request, tsid = None):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        spent_time = request.POST['spent_time']
        uid = request.session['uid']
        get_task_data_update(uid = uid, task_id = tsid, title = title, description = description, spent_time = spent_time)
        return redirect(emp_task)
    try:    
        uid = request.session['uid']
        fm_data = get_task_data(uid = uid, task_id = tsid)
        update_form = TaskForm(fm_data)
        return render(request, 'update_task.html' , {"form" : update_form})
    except:
        return render(request, 'login.html')

def delete_task(request, tsid = None):
    uid = request.session['uid']
    fire_db.child("users").child(uid).child("tasks").child(tsid).remove()
    return redirect(emp_task)
