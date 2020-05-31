from django.db import models

# Create your models here.
class Location(models.Model):
    state= models.CharField(max_length=60, null=True)
    city = models.CharField(max_length=60)
    latitude = models.DecimalField(max_digits=8,decimal_places=4)
    longitude = models.DecimalField(max_digits=8,decimal_places=4)
    farm = models.TextField()

    def __str__(self):
        return str(self.city+", "+self.state)

class Product(models.Model):
    name = models.CharField(max_length=100)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    price = models.IntegerField()
    image = models.ImageField(upload_to="shop/images")     

    def __str__(self):
        return self.name






