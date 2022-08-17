from django.contrib.auth import logout, login, authenticate,forms
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.urls import reverse
from . import models
from scipy import stats
import numpy as np
#login_required
def main(request):
    return render(request, 'registration/main.html',{})

def home(request):
    return render(request,'registration/home.html',{})

def logout_request(request):
    logout(request)
    return redirect('login')

def signup(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        login(request,user)
        return redirect('login')
    return render(request, 'registration/signup.html', {'form': form})

def password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect('home')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/password.html', {
        'form': form
    })

def create(request):
    if request.method == 'POST':
        dictionary = request.POST
        print(dictionary)
        form = models.Survey()
        form.title = dictionary.get('title')
        form.owner = request.user
        form.save()
        for key, value in dictionary.items():
            lst = key.split("$")
            if len(lst) == 2:
                if lst[1] == "1":
                    question = models.Line()
                    question.question_number = lst[0].split('@')[1]
                    question.question_type = 1
                    question.question = value
                    question.question_valid = lst[0].split('@')[0]
                    question.form = form 
                    question.save()
                elif lst[1] == "2":
                    question = models.Para()
                    question.question_number = lst[0]
                    question.question_type = 2
                    question.question = value
                    question.form = form 
                    question.save()
                elif lst[1] == "3":
                    question = models.Single()
                    question.question_number = lst[0]
                    question.question_type = 3
                    question.question = value
                    question.form = form 
                    question.save()
                elif lst[1] == "4":
                    question = models.Multi()
                    question.question_number = lst[0]
                    question.question_type = 4
                    question.question = value
                    question.form = form 
                    question.save()
                elif lst[1] == "5":
                    question = models.Drop()
                    question.question_number = lst[0]
                    question.question_type = 5
                    question.question = value
                    question.form = form
                    question.save()
                elif lst[1] == "6":
                    question = models.File()
                    question.question_number = lst[0].split('@')[1]
                    question.question_type = 6
                    question.question = value
                    question.question_valid = lst[0].split('@')[0]
                    question.form = form 
                    question.save()
                elif lst[1] == "7":
                    question = models.Toggle()
                    question.question_number = lst[0]
                    question.question_type = 7
                    question.question = value
                    question.form = form 
                    question.save()
                elif lst[1] == "8":
                    question = models.Slider()
                    question.question_number = lst[0]
                    question.question_type = 8
                    question.question = value
                    question.form = form 
                    question.save()
        for key, value in dictionary.items():
            lst = key.split('$')
            if len(lst) == 3:
                print(lst)
                print(value)
                if lst[1] == "3":
                    option = models.Single_option()
                    option.option = value
                    option.option_number = lst[2]
                    option.template = models.Single.objects.filter(form = form, question_number = lst[0])[0]
                    option.save()
                elif lst[1] == "4":
                    option = models.Multi_option()
                    option.option = value
                    option.option_number = lst[2]
                    option.template = models.Multi.objects.filter(form = form, question_number = lst[0])[0]
                    option.save()
                elif lst[1] == "5":
                    option = models.Drop_option()
                    option.option = value
                    print(option.option)
                    option.option_number = lst[2]
                    option.template = models.Drop.objects.filter(form = form, question_number = lst[0])[0]
                    option.save()
        return redirect('home')
    return render(request,'form.html', {})

def formlist(request):
    lst = models.Survey.objects.filter(owner=request.user)
    base_url=reverse('main')
    return render(request, 'list.html', {'list': lst, 'base_url': base_url})

def displayform(request,pk):
    myform = models.Survey.objects.get(pk=pk)
    q_lst = list(models.Line.objects.filter(form = myform)) + list(models.Para.objects.filter(form = myform)) +list(models.Single.objects.filter(form = myform)) +list(models.Multi.objects.filter(form = myform)) +list(models.Toggle.objects.filter(form = myform)) + list(models.Drop.objects.filter(form = myform)) +list(models.Slider.objects.filter(form = myform)) +list(models.File.objects.filter(form = myform))
    q_lst.sort(key=lambda x: x.question_number)
    mylist = []
    for x in q_lst:
        if isinstance(x,models.Line):
            mylist.append([x,[]])
        elif isinstance(x,models.Para):
            mylist.append([x,[]])
        elif isinstance(x,models.File):
            mylist.append([x,[]])
        elif isinstance(x,models.Slider):
            mylist.append([x,[]])
        elif isinstance(x,models.Toggle):
            mylist.append([x,[]])
        elif isinstance(x,models.Single):
            temp = list(models.Single_option.objects.filter(template = x).order_by('option_number'))
            mylist.append([x,temp])
        elif isinstance(x,models.Multi):
            temp = list(models.Multi_option.objects.filter(template = x).order_by('option_number'))
            mylist.append([x,temp])
        elif isinstance(x,models.Drop):
            temp = list(models.Drop_option.objects.filter(template = x).order_by('option_number'))
            mylist.append([x,temp])
    return render(request,"displayform.html", {"mylist": mylist, "form": myform})

def answer(request,pk):
    myform = models.Survey.objects.get(pk=pk)
    q_lst = list(models.Line.objects.filter(form = myform)) + list(models.Para.objects.filter(form = myform)) +list(models.Single.objects.filter(form = myform)) +list(models.Multi.objects.filter(form = myform)) +list(models.Toggle.objects.filter(form = myform)) + list(models.Drop.objects.filter(form = myform)) +list(models.Slider.objects.filter(form = myform)) +list(models.File.objects.filter(form = myform))
    q_lst.sort(key=lambda x: x.question_number)
    mylist = []
    for x in q_lst:
        if isinstance(x,models.Line):
            mylist.append([x,[]])
        elif isinstance(x,models.Para):
            mylist.append([x,[]])
        elif isinstance(x,models.File):
            mylist.append([x,[]])
        elif isinstance(x,models.Slider):
            mylist.append([x,[]])
        elif isinstance(x,models.Toggle):
            mylist.append([x,[]])
        elif isinstance(x,models.Single):
            temp = list(models.Single_option.objects.filter(template = x).order_by('option_number'))
            mylist.append([x,temp])
        elif isinstance(x,models.Multi):
            temp = list(models.Multi_option.objects.filter(template = x).order_by('option_number'))
            mylist.append([x,temp])
        elif isinstance(x,models.Drop):
            temp = list(models.Drop_option.objects.filter(template = x).order_by('option_number'))
            mylist.append([x,temp])
    if request.method == 'POST':
        dictionary = request.POST
        print(dictionary)
        for key, value in dictionary.items():
            lst = key.split("@")
            if len(lst) == 2:
                if lst[0] == "1":
                    answer = models.Line_response()
                    answer.parent_question = models.Line.objects.filter(id = lst[1])[0]
                    answer.answer = value
                    answer.owner = request.user 
                    answer.save()
                elif lst[0] == "2":
                    answer = models.Para_response()
                    answer.parent_question = models.Para.objects.filter(id = lst[1])[0]
                    answer.answer = value
                    answer.owner = request.user 
                    answer.save()
                elif lst[0] == "3":
                    answer = models.Single_response()
                    answer.parent_question = models.Single.objects.filter(id = lst[1])[0]
                    answer.parent_option = models.Single_option.objects.filter(id = value)[0]
                    answer.owner = request.user 
                    answer.save()
                elif lst[0] == "4":
                    if(value == "on"):
                        answer = models.Multi_response()
                        answer.parent_question = models.Multi.objects.filter(id = lst[1].split('#')[0])[0]
                        answer.parent_option = models.Multi_option.objects.filter(id = lst[1].split('#')[1])[0]
                        answer.owner = request.user 
                        answer.save()
                elif lst[0] == "5":
                    answer = models.Drop_response()
                    answer.parent_question = models.Drop.objects.filter(id = lst[1])[0]
                    answer.parent_option = models.Drop_option.objects.filter(id = value)[0]
                    answer.owner = request.user 
                    answer.save()
                elif lst[0] == "6":
                    answer = models.File_response()
                    answer.parent_question = models.File.objects.filter(id = lst[1])[0]
                    answer.answer = value
                    answer.owner = request.user 
                    answer.save()
                elif lst[0] == "7":
                    answer = models.Toggle_response()
                    answer.parent_question = models.Toggle.objects.filter(id = lst[1])[0]
                    if value=="on":
                        answer.answer = 1
                    else:
                        answer.answer = 0
                    answer.owner = request.user 
                    answer.save()
                elif lst[0] == "8":
                    answer = models.Slider_response()
                    answer.parent_question = models.Slider.objects.filter(id = lst[1])[0]
                    answer.answer = value
                    answer.owner = request.user 
                    answer.save()
        return redirect('home')
    return render(request,"answer.html", {"mylist": mylist, "form": myform})

def question(request,pk):
    if request.method == 'POST':
        m1=0
        m2=0
        m3=0
        dictionary = request.POST
        check = 0
        #print(dictionary)
        myform = models.Survey.objects.get(pk=pk)
        #print(myform)
        for key,value in dictionary.items():
            q = key.split('_')
            if len(q)==2:
                lst_1 = list(models.Line_response.objects.filter(parent_question__question_number = value, parent_question__form = myform, parent_question__question_valid = '2'))
                
                lst_1= [int(x.answer) for x in lst_1]
                if len(lst_1)>0:
                    check =1
                    print(check)
                    a =np.array(lst_1)
                    m1 = np.mean(a)
                    m2 = np.median(a)
                    m3 = stats.mode(a)
                    m4 = m3[0]
                    print(m4)
                a_lst = list(models.Single_response.objects.filter(parent_question__question_number = value)) +list(models.Multi_response.objects.filter(parent_question__question_number = value))+ list(models.Drop_response.objects.filter(parent_question__question_number=value))
                #print(a_lst)
                o_lst = list(models.Single_option.objects.filter(template__question_number =value,template__form = myform)) +list(models.Multi_option.objects.filter(template__question_number =value,template__form = myform))+ list(models.Drop_option.objects.filter(template__question_number =value,template__form = myform))
                #print(o_lst)
                lst2 = [i.option_number for i in o_lst]
                lst1 = [i.parent_option.option_number for i in a_lst]
                lst5 = [[i,lst1.count(i)] for i in lst2]
        return render(request,"visualize.html",{"lst":lst5,"mean":m1,"median":m2,"mode":m4,"checkno":check})
    return render(request,"question.html", {})
