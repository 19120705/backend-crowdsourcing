from django.db import models
from django.conf import settings
from django.utils import timezone




# Create your models here.

class ModelBase (models.Model):
    class Meta:
        abstract = True

    subject = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.subject

    
# Type of project
class Category (models.Model):
    name = models.CharField(max_length=255, null=False)
    def __str__(self):
        return self.name
# Type of label        
class Type_label (models.Model):
    name = models.CharField(max_length=255, null=False)
    category = models.ForeignKey(Category,on_delete=models.PROTECT, related_name="category_label", default=1)
    def __str__(self):
        return self.name


class Project (ModelBase):
    class Meta:
        unique_together = ('subject', 'category')
        ordering = ["-id"]

    description = models.CharField(max_length=500)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, default=1)
    
    size = models.IntegerField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Tag(models.Model):
    name = models.CharField(max_length=50)
    project = models.ForeignKey(Project,on_delete=models.PROTECT, related_name="tag_project", default=1)
    def __str__(self):
        return self.name





class Data (models.Model):
    class Meta:
        abstract = True
    type_label = models.ForeignKey(Type_label, on_delete=models.PROTECT, related_name="%(class)s_label")   
    project = models.ForeignKey(Project,on_delete=models.PROTECT, related_name="%(class)s_project")


class Document (Data):
    content = models.CharField(max_length=500)
    
class Question (Data):
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)

class Text_pair (Data):
    paragraph_1 = models.CharField(max_length=500)
    paragraph_2 = models.CharField(max_length=500)


class Action (models.Model):
    class Meta:
        abstract = True
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project,on_delete=models.PROTECT, related_name="%(class)s_project")


class Action_Question (Action):
    MY_CHOICES = (
        ('yes', 'Yes'),
        ('no', 'No'),
        ('maybe', 'Maybe')
    )
    question = models.ForeignKey(Question, on_delete=models.PROTECT, related_name="action_question")   
    tag = models.CharField(max_length=10, choices=MY_CHOICES)

class Action_Document (Action):
    document = models.ForeignKey(Document, on_delete=models.PROTECT, related_name="action_document")   
    tag = models.ManyToManyField(Tag)

class Action_TextPair (Action):
    TEXT_CHOICES = (
        ('synonymous', 'synonymous'),
        ('opposite', 'opposite')
    )
    text_pair = models.ForeignKey(Text_pair, on_delete=models.PROTECT, related_name="action_textpair")   
    tag = models.CharField(max_length=20, choices=TEXT_CHOICES)