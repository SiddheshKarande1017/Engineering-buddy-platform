from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models
# Create your models here.

class Problem(models.Model):
    q_id = models.AutoField(primary_key=True)
    topic = models.CharField(max_length=30)
    q_name = models.CharField(max_length=30,unique = True)
    link = models.URLField(max_length=200,unique = True)

class Sources(models.Model):
    id = models.AutoField(primary_key=True)
    topic = models.CharField(max_length=30)
    link = models.URLField(max_length=200)



class UploadedDoc(models.Model):
        doc_file = models.FileField(upload_to='docs/')
        extracted_text = models.TextField(blank=True)
