from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models

CATEGORIES = (
    ('a', 'Accessories'),
    ('b', 'Homeware'),
    ('c', 'Electronics'),
    ('d', 'Gardenware'),
    ('e', 'Kitchenware'),
    ('f', 'Miscellaneous'),
)


class User(AbstractUser):
    pass


class Bid(models.Model):
    time = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_bids")
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user} placed a bid of ${self.price}"


class Comment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_coms")
    title = models.CharField(max_length=25, default="")
    comment = models.CharField(max_length=255)
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user}: {self.comment}"


class Listing(models.Model):
    item = models.CharField(max_length=64)
    description = models.CharField(max_length=255, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(
        max_length=1, choices=CATEGORIES, default=CATEGORIES[5][1])
    time = models.DateTimeField(default=timezone.now)
    closed = models.BooleanField(default=False)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owners")
    bids = models.ManyToManyField(Bid, blank=True, related_name="bids")
    comments = models.ManyToManyField(
        Comment, blank=True, related_name="comments")
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return f"{self.item}: listed at: {self.price} sold by: {self.owner}"


class Watchlist(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="listings")

    def __str__(self):
        return f"{self.user.username} listed {self.listing.id}"
