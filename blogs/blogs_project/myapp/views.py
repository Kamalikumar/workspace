# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.core.validators import RegexValidator

from .form import Todo_forms
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Todo
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError


def index(request):
    return HttpResponse('Welcome to Todo app in Django')

@login_required
def suggestion(request):

    items = Todo.objects.filter(user=request.user).order_by('-id')


    print "------->", request.GET

    f_completed = Todo.objects.filter(user=request.user, is_completed=False)
    t_completed = Todo.objects.filter(user=request.user, is_completed=True)

    # name = request.user
    # print "==========>",name
    search = request.GET.get('i_text')

    if search:
        s_text = Todo.objects.filter(text__contains=search,user=request.user)
        if s_text:
            return render(request, 'myapp/basic.html', context={'items': s_text,},)

    if request.GET.get('items')=='f_completed':
        return render(request,'myapp/basic.html',context=  {'items': f_completed,},)

    if request.GET.get('items')=='t_completed':
        return render(request,'myapp/basic.html',context=  {'items': t_completed,},)

    if request.GET.get('items')=='All':
        return render(request,'myapp/basic.html',context=  {'items': items,},)


    if request.method == "POST":
        form = Todo_forms(request.POST)
        if form.is_valid():
            try:
                d_s=form.save(commit=False)
                d_s.user =request.user
                d_s.save()
                messages.success(request, "Your Todo list is Successfully saved")
            except IntegrityError as e:
                messages.error (request,"Already exists")
            return render(request, 'myapp/basic.html', context={'items': items,}, )

        else:
            error= form.errors
            print "------>", error
            return HttpResponse(error)
    return render(request,'myapp/basic.html',context= {'items': items},)
    #return HttpResponseRedirect('/todo')


def update(request,task_id):
    items = Todo.objects.all()
    q = get_object_or_404(Todo, pk=task_id)
    form = Todo_forms(request.POST)
    if request.method == "POST":
            print "----->", q
            q.is_completed = not q.is_completed
            q.save()
    return HttpResponseRedirect('/todo')


def delete_list(request, task_id):
    c = get_object_or_404(Todo, pk=task_id)
    if request.method == "POST":
        print'===========>', c
        if c.is_completed == True:
            c.delete()
        else:
            print'Task not completed'
    return HttpResponseRedirect('/todo')


def password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            print"-------->", user
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/todo')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/password.html', {
        'form': form
    })

def set_timezone(request):
    items = Todo.objects.filter(user=request.user).order_by('-id')
    form = Todo(request.POST)

def edit_post(request, pk):
    items = Todo.objects('id')
    template = 'myapp/basic.html'
    post = get_object_or_404(Todo, pk=pk)

    if request.method == 'POST':
        form = Todo_forms(request.POST, instance=post)

        try:
            if form.is_valid():
                form.save()
                messages.success(request, "Your Blog Post Was Successfully Updated")

        except Exception as e:
            messages.warning(request, 'Your Post Was Not Saved Due To An Error: {}'.format(e))

    else:
        form = Todo_forms(instance=post)

    return render(request, template, context= {'items': items},)



def get_detail(request, pk):
    movie = Todo.Movies(pk)
    response = movie.info()
    context = {
        'response': response
    }
    return render(request, './moviecompare/detail.html', context)
