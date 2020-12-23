from django.db import models
from django.contrib.auth.models import AbstractUser
from taggit.managers import TaggableManager

class Newuser(AbstractUser):
    profilepic=models.FileField(upload_to='media/userprofile',blank=False,null=True)
    questioncount=models.IntegerField(blank=True,null=True)
    answercount=models.IntegerField(blank=True,null=True)
    suspendreason=models.TextField(blank=True,null=True)
    

class Userfollowing(models.Model):
    user_id=models.ForeignKey("Newuser",related_name="followers" ,on_delete=models.CASCADE)
    following_user_id=models.ForeignKey("Newuser",related_name="following" ,on_delete=models.CASCADE)
    class Meta:
        constraints=[models.UniqueConstraint(fields=['user_id','following_user_id'],name="unique_followers")] 
    def __str__(self):
        return self.user_id.username+" : follows : "+self.following_user_id.username
    
class Question(models.Model):
    title=models.CharField(max_length=100,null=False,blank=False,unique=True)
    discription=models.TextField(max_length=1000,null=False,blank=False)
    file=models.FileField(upload_to="media/question" ,blank=True,null=True)
    askedby=models.ForeignKey(Newuser,on_delete=models.CASCADE)
    report=models.BooleanField(default=False)
    questiondate=models.DateTimeField(auto_now_add=True)
    slug=models.SlugField(max_length=100)
    tags=TaggableManager()
    answers=models.IntegerField(default=0)
    like_users = models.ManyToManyField('Newuser', through='Likes', related_name='liked_posts')
    dislike_users = models.ManyToManyField('Newuser', through='Dislikes', related_name='disliked_posts')
    def __str__(self):
        return str(self.title)+" : "+str(self.askedby)
    
class Likes(models.Model):
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    likesby=models.ForeignKey(Newuser,on_delete=models.CASCADE)
    
class Dislikes(models.Model):
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    dislikesby=models.ForeignKey(Newuser,on_delete=models.CASCADE)          


class Answer(models.Model):
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    answerby=models.ForeignKey(Newuser,on_delete=models.CASCADE)
    discription=models.TextField(max_length=1000,null=True,blank=False)
    file=models.FileField(upload_to="assert/answer" , blank=True,null=True)
    report=models.BooleanField(default=False)  
    answerdatedate=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.question)+" : "+str(self.answerby)