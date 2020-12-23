from django.contrib import admin
from .models import Newuser,Question,Answer,Likes,Userfollowing

admin.site.register(Newuser)
admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(Likes)
admin.site.register(Userfollowing)