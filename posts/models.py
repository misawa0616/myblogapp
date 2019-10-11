from django.db import models

# Create your models here.
class Post(models.Model):
	titie = models.CharField(max_length=100)
	published = models.DateTimeField()
	image = models.ImageField(upload_to='media/')
	body = models.TextField()

	def __str__(self):
		return self.titie

	def summary(self):
		return self.body[:30]