from django.db import models
from listing.models import Listing
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Mark:
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5
    marks = (
        (one, 'Too bad!'),
        (two, 'Bad!'),
        (three, 'Normal!'),
        (four, 'Good!'),
        (five, 'Excelent!')
    )

class Review(models.Model):
    product = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    rating = models.IntegerField(choices=Mark.marks)
    created_at = models.DateTimeField(auto_now_add=True)
