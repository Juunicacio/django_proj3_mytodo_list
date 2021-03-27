"""mytodo_list URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from todo_app import views
# to see images in the static folder
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication
    path('signup/', views.signupuser, name='signupuser'),
    path('login/', views.loginuser, name='loginuser'),
    path('logout/', views.logoutuser, name='logoutuser'),

    # Todo stuff
    path('', views.home, name='home'),
    # to the user be able to create a new todo
    path('createtodo/', views.createtodo, name='createtodo'),
    path('mytodos/', views.mytodos, name='mytodos'),
    path('completed/', views.mycompletedtodos, name='mycompletedtodos'),
    # taking a primary key for that specific todo
    path('todo/<int:todo_pk>', views.updatetodo, name='updatetodo'),
    path('todo/<int:todo_pk>/complete', views.completetodo, name='completetodo'),
    path('todo/<int:todo_pk>/delete', views.deletetodo, name='deletetodo'),

    # Draw stuff
    path('draw/', views.draw, name='draw'),
]
