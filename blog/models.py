from django.db import models

# Create your models here.
class blogPost(models.Model):
    blog_id = models.AutoField(primary_key=True)
    head1 = models.CharField(max_length=500)
    subhead1 = models.CharField(max_length=5000, default="")
    head2 = models.CharField(max_length=500)
    subhead2 = models.CharField(max_length=5000, default="")
    head3 = models.CharField(max_length=500)
    subhead3 = models.CharField(max_length=5000, default="")
    Location = models.CharField(max_length=100)
    image = models.ImageField(upload_to='shop/images', default="")
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.head1