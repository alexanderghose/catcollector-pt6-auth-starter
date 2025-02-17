from django.db import models
from django.urls import reverse

MEALS = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner')
)

class Toy(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('toy-detail', kwargs={'pk': self.id})

# Create your models here.
# this is the django parallel of
# creating mongoose schemas
class Cat(models.Model):
    name = models.CharField(max_length=100) # add a name column
    breed = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()
    toys = models.ManyToManyField(Toy)

    def __str__(self): # helps us have better prints of cats
        return self.name
    
    # Define a method to get the URL for this particular cat instance
    def get_absolute_url(self):
        # Use the 'reverse' function to dynamically find the URL for viewing this cat's details
        return reverse('cat-detail', kwargs={'cat_id': self.id})


class Feeding(models.Model):
    date = models.DateField("Feeding Date")
    meal = models.CharField(max_length=1, choices=MEALS, default='B')
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_meal_display()} on {self.date}"

    # Define the default order of feedings
    class Meta:
        ordering = ['-date']  # This line makes the newest feedings appear first

