from django.shortcuts import render,get_object_or_404,redirect
from .models import Question,Answer,Newuser,Likes,Userfollowing
from allauth.account.decorators import login_required
from .forms import Questionform,Answerform,Profileform
from taggit.models import Tag
from django.template.defaultfilters import slugify
from django.contrib import messages
from .extra import basecontext


def follow(request):
    user=request.user
    context=basecontext(request)
    f=request.GET['follow']
    if "-" in f:
        f=f.lstrip("-")
        usertoberemoved=Userfollowing.objects.get(user_id=user,following_user_id=Newuser.objects.get(id=f))
        usertoberemoved.delete()
        print("user follow delted")
         #Userfollowing.objects.delete(following_user_id=Newuser.objects.get(id=f))
        
    else:
     
        Userfollowing.objects.create(user_id=user,following_user_id=Newuser.objects.get(id=f))
        print("user follow created")
        
        
   
    profileform = Profileform(initial={'first_name': user.first_name, 
                                         'last_name': user.last_name, 
                                            
                                             'profilepic': user.profilepic})

    count=len(Question.objects.filter(askedby=user))
    user.questioncount=count
    count=len(Answer.objects.filter(answerby=user))
    user.answercount=count
    user.save()
    
    context['profileform']=profileform
    context['profile']=Newuser.objects.get(username=user)
    return render(request,"profileform.html",context=context)

@login_required
def likes(request):
    
    user=request.user
    id=request.GET['question']
    
    if "-" in id:
        question=Question.objects.get(id=id.lstrip("-"))
        if question.like_users.filter(username=user.username).count()>0:
            question.like_users.remove(user)
        else:
            question.dislike_users.add(user)
        
    else:
        question=Question.objects.get(id=id)
        if question.dislike_users.filter(username=user.username).count()>0:
                question.dislike_users.remove(user)
        else:
            question.like_users.add(user)
        context=basecontext(request)        
    question.save()
    
    questions=Question.objects.filter().order_by("-questiondate")
    context=basecontext(request)
    context.update({'questions':list(questions)})
    return render(request,"home-twocolumn.html",context=context)


@login_required
def myprofile(request):
    context=basecontext(request)
    user=request.user
    if request.method=="POST":
        profileformdat=Profileform(request.POST,request.FILES)
        
        if profileformdat.is_valid():
            profile=Newuser.objects.get(id=request.user.id)
            profile.first_name=profileformdat.cleaned_data['first_name']
            profile.last_name=profileformdat.cleaned_data['last_name']
            profile.profilepic=request.FILES['profilepic']
            profile.save()
            return redirect("/myprofile")
        else:
            context['profileform']=Profileform(request.POST)
            context['profile']=Newuser.objects.get(username=user)
    else:         
        
        profileform = Profileform(initial={'first_name': user.first_name, 
                                         'last_name': user.last_name, 
                                            
                                             'profilepic': user.profilepic})

        count=len(Question.objects.filter(askedby=user))
        user.questioncount=count
        count=len(Answer.objects.filter(answerby=user))
        user.answercount=count
        user.save()
       
        context['profileform']=profileform
        context['profile']=Newuser.objects.get(username=user)
    return render(request,"profileform.html",context=context)


@login_required
def deskboard(request):
    context=basecontext(request)
    questions=Question.objects.filter(askedby=request.user).order_by("-answers")
    answerlist=Answer.objects.filter(answerby=request.user)
    commontags=Question.tags.most_common()[:10]
    context['answerlist']=answerlist
    context['questions']=questions
    return render(request,"home-twocolumn.html",context=context)


def answerlist(request):
    context=basecontext(request)
    questionid=request.GET['id']
    question=Question.objects.get(id=questionid)
    answerlist=Answer.objects.filter(question=question)
    context['answerlist']=answerlist
    context['question']=question
    return render(request,"answerlist.html",context=context)

@login_required
def answer(request):
    context=basecontext(request)

    
    if request.method=="POST":
        answerformdata=Answerform(request.POST,request.FILES)
        if answerformdata.is_valid():
            question=get_object_or_404(Question,id=request.session['question_id'])
            newanwer=answerformdata.save(commit=False)
            newanwer.answerby=request.user
            newanwer.question=question
            sameuseranslist=Answer.objects.filter(question=question,answerby=request.user)
            if len(sameuseranslist)>0:
                sameuseranslist.delete()
            else:    
                question.answers+=1
                question.save()
            newanwer.save()    
            
            

            return redirect('/')
        else:
            question=answerformdata.fields['question']
            answerform=Answerform(answerformdata)
            context.update({'answerform':answerform})        
            context.update({'question':Question.objects.get(id=question.id)})
               
    else:
        id=request.GET['id']
        request.session['question_id']=id
        question=get_object_or_404(Question,id=id)
        answerform=Answerform(initial={'question':question})

        context.update({'answerform':answerform})
        context.update({'question':question})
    return render(request,"answer.html",context=context)
    

def home(request):
   
    questions=Question.objects.filter().order_by("-questiondate")
    context=basecontext(request)
    context.update({'questions':list(questions)})
    
    return render(request,"home-twocolumn.html",context=context)


@login_required
def question(request):
    context=basecontext(request)
    if request.method=="POST":        
        questionform=Questionform(request.POST,request.FILES)
        
        
        if questionform.is_valid():
            questionform=Questionform(request.POST)

            newquestion=questionform.save(commit=False)
            newquestion.slug=slugify(newquestion.title)
            newquestion.askedby=request.user
            newquestion.save()
            questionform.save_m2m()
            messages.success(request,"New Question submitted")
            questions=Question.objects.all().order_by("-questiondate")
            context.update({'questions':questions})

            return render(request,"home-twocolumn.html",context=context)
        else:
            questionform=Questionform(request.POST)    
            context.update({'questionform':questionform})
             
    else:
        questionform=Questionform()
        context.update({'questionform':questionform})
    return render(request,"question.html",context=context)



def taged(request,ta):
    
    tag = get_object_or_404(Tag, slug=ta)
    context=basecontext(request)
    questions=Question.objects.filter(tags=tag)    
    context.update({'questions':questions})
    return render(request,"home-twocolumn.html",context=context)


def slug(request,sl):
    context=basecontext(request)
  
  
    context['questions']=Question.objects.filter(slug=sl)
    return render(request,"home-twocolumn.html",context=context)
