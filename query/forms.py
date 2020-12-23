from .models import Question,Answer
from django import forms
from .models import Newuser
from django.utils.translation import gettext_lazy as _

class Questionform(forms.ModelForm):
    
    def clean_tags(self):
        datalist = self.cleaned_data['tags']
        for data in datalist:
            if not( data.isalnum() or "-" in data): 
                 raise forms.ValidationError("Tags should not have special characters.")
            return datalist
    
    
    class Meta:
        model= Question
        fields=['title','discription','file',"tags"]
        widgets={
            'title':forms.TextInput(attrs={'class':"form-control",'placeholder':"Please Enter title of your Question"}),
            'discription':forms.Textarea(attrs={"class":"form-control xyz",'placeholder':"Please Enter Detailed distription of your Question","id":"validationTextarea"}),
            'tags':forms.TextInput(attrs={"class":"form-control",'name':'tags','data-role':'tagsinput'})
    
        }
        labels={
            'file':_("Attachement")
                }   
        error_messages={
            'title':{'max_length':_('title must me less that 100 charcters'),}  
                        }  
            
class Profileform(forms.ModelForm):
    class Meta:
        model =Newuser
        fields=['first_name','last_name','profilepic']
        
        
        
class Answerform(forms.ModelForm):

    class Meta:
        model= Answer
    
        fields=['discription','file']
        widgets={
            'discription':forms.Textarea(attrs={"class":"form-control xyz",'placeholder':"Please Enter Detailed distription of your Question","id":"answertestarea"}),
    
        }
        
        labels={
            'file':_("Attachement")
                }
       
        error_messages={
            'discription':{'max_length':_('title must me less that 100 charcters'),}  
                        }  
            
        