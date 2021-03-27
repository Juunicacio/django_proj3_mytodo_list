# to get an object from the database import get_object_or_404
from django.shortcuts import render, redirect, get_object_or_404
# django form for creation and for authentication
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# django model for User
from django.contrib.auth.models import User
# IntegrityError for unique username
from django.db import IntegrityError
# login and logout
from django.contrib.auth import login, logout, authenticate
# import that form that you've created in myforms.py file
from .myForms import TodoForm
# import Todo model for database
from .models import Todo
# import timezone
from django.utils import timezone
# only logged in users can have access to certain pages
from django.contrib.auth.decorators import login_required
# in settings say where you want to direct that error page

def home(request):
    return render(request, 'todo/index.html')

def signupuser(request):
    # Check if is as GET or POST request, cause we have a POST form
    if request.method == 'GET':
        # For sign up we use the UserCreationForm()
        return render(request, 'todo/signupuser.html', {'form':UserCreationForm()})
    else:
        # Check if both password1 and password2 are the same
        if request.POST['password1'] == request.POST['password2']:
            # Now see if the username is unique
            try:
                # Create a new user object
                user = User.objects.create_user(request.POST['username'], password= request.POST['password1'])
                # Save into the database
                user.save()
                # Login the user after the user creation
                login(request, user)
                # After login, return a redirect to the user to their 'todos' page
                return redirect('mytodos')

            # When the username is not unique
            except IntegrityError:
                # Return the user to the form and tell that the username has already been taken through the dictionary
                return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':'That username has already been taken. Please choose a new username.'})

        else:
            # Return the user to the form and tell that the passwords didn't match through the dictionary
            return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':'Passwords did not match'})

def loginuser(request):
    # Check if is as GET or POST request, cause we have a POST form
    if request.method == 'GET':
        # For login we use the AuthenticationForm()
        return render(request, 'todo/loginuser.html', {'form':AuthenticationForm()})
    else:
        # Check if the user is authenticate
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        # If it doesn't match, the user will be = to None
        if user is None:
            # send them back to the login page, but with an error
            return render(request, 'todo/loginuser.html', {'form':AuthenticationForm(), 'error':'Username and Password did not match.'})
        else:
            # We were able to authenticate them, so we just want to log them in
            login(request, user)
            # After login, return a redirect to the user to their 'todos' page
            return redirect('mytodos')
@login_required
def logoutuser(request):
    # We just want to logout if it is a post request, cause if someone goes to /logout/ with GET, they will automatically be kicked out
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required
def createtodo(request):
    if request.method == 'GET':
        # we need a form that have all the columns we needed for the model
        # use that form that you've created in myforms.py file
        return render(request, 'todo/createtodo.html', {'form':TodoForm()})
    else:
        try:
            # take the info from POST and connect it to the form
            form = TodoForm(request.POST)
            # crate a new object for me and don't put it into the db yet
            # put into a variable and specify the user, that is missing
            newTodo = form.save(commit=False)
            newTodo.createdByUser = request.user
            # now we can save into the database
            newTodo.save()
            # send it to the page so the user can see it
            return redirect('mytodos')
        # if the user try to type more info than it is permited in the lenght, give them a error msg        
        except ValueError:
            # give them back the same form with the error
            return render(request, 'todo/createtodo.html', {'form':TodoForm(), 'error': 'Bad data passed in, please try again.'})

@login_required
def mytodos(request):
    # we need to get all the todo objects from the database
    # if we pass Todo.objects.all() we get all objs not just those from the user
    # if I've completed one todo, it should not be seen, so it is not null anymore, is will not be seen
    todos = Todo.objects.filter(createdByUser=request.user, completedAt__isnull=True)
    # pass the todos into our template with a dict
    return render(request, 'todo/mytodos.html', {'todos':todos})

@login_required
def draw(request):
    return render(request, 'todo/draw.html')

@login_required
def mycompletedtodos(request):
    todos = Todo.objects.filter(createdByUser=request.user, completedAt__isnull=False).order_by('-completedAt')
    return render(request, 'todo/mycompletedtodos.html', {'todos':todos})

@login_required
def updatetodo(request, todo_pk):
    # grab single todo from the database
    # we have to make sure that that object comes from that specific user
    # pass the class we are looking for and what the pk should be equal to
    todo = get_object_or_404(Todo, pk=todo_pk, createdByUser=request.user)
    # if the user does not match, it will return a 404 page
    if request.method == 'GET':
        # we need to display a todo form, but we need to use a todo form that is filled already with the todo data
        form = TodoForm(instance=todo)
        # pass into the dict also the form
        return render(request, 'todo/updatetodo.html', {'todo':todo, 'form':form})
    else:
        try:
            # pass the request form and the user with instance=todo
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('mytodos')
        except ValueError:
            return render(request, 'todo/updatetodo.html', {'todo':todo,'form':form, 'error': 'Bad data passed in, please try again.'})

@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, createdByUser=request.user)
    # make sure that it is a POST
    if request.method == 'POST':
        todo.completedAt = timezone.now()
        todo.save()
        return redirect('mytodos')

@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, createdByUser=request.user)
    # make sure that it is a POST
    if request.method == 'POST':
        todo.delete()
        return redirect('mytodos')

