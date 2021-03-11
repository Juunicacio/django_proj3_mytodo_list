from django.shortcuts import render, redirect
# django form for creation and for authentication
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# django model for User
from django.contrib.auth.models import User
# IntegrityError for unique username
from django.db import IntegrityError
# login and logout
from django.contrib.auth import login, logout, authenticate

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

def mytodos(request):
    return render(request, 'todo/mytodos.html')

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

def logoutuser(request):
    # We just want to logout if it is a post request, cause if someone goes to /logout/ with GET, they will automatically be kicked out
    if request.method == 'POST':
        logout(request)
        return redirect('home')