from django.db import models


# Create your models here.

class Blogpost(models.Model):
    post_id = models.AutoField(primary_key=True)
    thumbnail = models.ImageField(upload_to='blog/images', default="")
    title = models.CharField(max_length=100)
    head0 = models.CharField(max_length=500, default="")
    contentHead0 = models.CharField(max_length=5000, default="")
    head1 = models.CharField(max_length=500, default="")
    contentHead1 = models.CharField(max_length=5000, default="")
    head2 = models.CharField(max_length=500, default="")
    contentHead2 = models.CharField(max_length=5000, default="")
    publishDate = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
