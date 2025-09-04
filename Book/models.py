from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Book(models.Model):
  def __str__(self):
    return self.title
  GENRES = [
        ("fic", "Fiction"),
        ("nfic", "Non-fiction"),
        ("sci", "Sci-Fi"),
        ("fan", "Fantasy"),
        ("bio", "Biography"),
        ("oth", "Other"),
    ]
  owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='books', null=True, blank=True)
  title = models.CharField(max_length=200)                      # required
  author = models.CharField(max_length=200)                     # required
  gener = models.CharField(max_length=50, choices=GENRES, default="oth")
  rating = models.PositiveSmallIntegerField(null=True, blank=True)
  notes = models.TextField(blank=True)
  created_at = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    display_name = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.display_name or self.user.username

