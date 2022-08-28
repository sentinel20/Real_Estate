from django.db import models
from account.models import CustomUser


class Listing(models.Model):
    title = models.CharField(max_length=150)
    price = models.IntegerField()
    num_bedrooms = models.IntegerField()
    num_bathrooms = models.IntegerField()
    image = models.ImageField(upload_to='images', null=True, blank=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=13)
    
    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


# class Booking(models.Model):
#     hotel = models.ForeignKey(Hotel, related_name='bookings', on_delete=models.CASCADE)
#     user = models.ForeignKey(CustomUser, related_name='bookings', on_delete=models.CASCADE)
#     room = models.ForeignKey(Room, related_name='bookings', on_delete=models.CASCADE)
#     booking_datetime = models.DateTimeField(auto_now_add=True)
#     arrival_datetime = models.DateTimeField()
#     departure_datetime = models.DateTimeField()

class Comment(models.Model):
    owner = models.ForeignKey(CustomUser, related_name='comments', on_delete=models.CASCADE)
    product = models.ForeignKey(Listing, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.owner} -> {self.product} -> {self.created_at}'

class Like(models.Model):
    product = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='likes')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='liked')

    class Meta:
        unique_together = ['product', 'owner']


class Favorites(models.Model):
    product = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='favorites')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='favorites')

    class Meta:
        unique_together = ['product', 'owner']