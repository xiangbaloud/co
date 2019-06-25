from django.db import models
from django.utils import timezone

class Document(models.Model):
	docfile = models.FileField(upload_to='')
	docfile_upload_time = models.DateTimeField(auto_now=True, null=True, blank=True)