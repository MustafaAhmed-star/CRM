from django.db import models

# Create your models here.
class Lead(models.Model):
    source_choices =(
        ('YouTube','YouTube'),
        ('Google', 'Google',)
        ('Newsletter', 'Newsletter',)
    )
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)

    phoned = models.BooleanField(default =False)
    source = models.CharField(choices=source_choices)
    profile_picture=models.ImageField(blank=True ,null=True)
    special_files = models.FileField(blank=True ,null=True)
    