"""questionanswer URL Configuration

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
from . import views

urlpatterns = [
    path('',views.home,name='name'),
     path('question/',views.question,name='question'),
     path('answer/',views.answer,name='answer'),
      path('slug/<sl>',views.slug,name='slug'),
      path('tag/<ta>/',views.taged,name='tagged'),
      path('answerlist/',views.answerlist,name="answerlist"),
      path('mydeskboard/',views.deskboard,name="deskboard"),
      path('myprofile/',views.myprofile,name="myprofile"),
      path('likes/',views.likes,name="likes"),
       path('follow/',views.follow,name="follow"),
      
      
]


