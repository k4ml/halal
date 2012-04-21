from django.db import models

class Company(models.Model):
    name = models.TextField()

class Scrap(models.Model):
    url = models.TextField()
    content = models.TextField(blank=True)
    has_result = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

class Product(models.Model):
    name = models.TextField()
    expired = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    source = models.ForeignKey(Scrap)

class Keyword(models.Model):
    name = models.CharField(max_length=255)
    count = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u"%s" % self.name
