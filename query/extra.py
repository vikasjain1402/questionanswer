
from .models import Question,Answer,Newuser,Likes,Dislikes
from taggit.models import Tag


from django.core.paginator import Paginator
from django.shortcuts import render



def listing(request):
    contact_list = Contact.objects.all()
    paginator = Paginator(contact_list, 25) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'list.html', {'page_obj': page_obj})


def basecontext(request,tags=10):
    context={}
    user=request.user
    context.update({'user':user})
    commontags=Question.tags.most_common()[:tags]
    context.update({'commontags':commontags})
    
    recentquestions=Question.objects.all().order_by("-questiondate")
    for question in recentquestions:
        question.lik=Likes.objects.filter(question=question).count()- Dislikes.objects.filter(question=question).count()
    
    
    
    paginator=Paginator(recentquestions,10)
    page_number = request.GET.get('page',1)
    recentquestions = paginator.get_page(page_number)
    context.update({"recentquestions":recentquestions})
    
    
    mostanswered=Question.objects.filter().order_by('-answers')[:5]
    context.update({"mostanswered":mostanswered})
    return context