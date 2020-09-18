from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
from users.models import User

# Create your models here.
class Photo(models.Model):
    photo = models.ImageField(upload_to="photos/", null=True, blank=True)
    photo_thumb = ImageSpecField(source="photo", processors=[ResizeToFit(200,200)], format="JPEG", options={"quality": 80})
    photo_large = ImageSpecField(source="photo", processors=[ResizeToFit(800,800)], format="JPEG", options={"quality": 90})
    photo_by = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="user_photos", null=True, blank=True)
    photo_added_date = models.DateField(auto_now_add=True)
    camera = models.CharField(max_length=100, null=True, blank=True)
    is_user_favorite = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="user_favorites", null=True, blank=True)
    starred_by = models.ManyToManyField(to=User, related_name="starred_photos", blank=True)
    public_photo = models.BooleanField(default=True)


class Gallery(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    photos = models.ManyToManyField(to=Photo, related_name="gallery_photos", blank=True)
    gallery_of = models.ManyToManyField(to=User, related_name="gallery_users", blank=True)
    date_added = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    public_gallery = models.BooleanField(default=True)


class Comment(models.Model):
    comment_by = models.ForeignKey(to=User, on_delete=models.CASCADE ,related_name="user_comments", null=True, blank=True)
    comments = models.ForeignKey(to=Photo, on_delete=models.CASCADE, related_name="photo_comments", null=True, blank=True)
    body = models.TextField(null=False, blank=False)
    comment_date = models.DateTimeField(auto_now_add=True)


class Pinned(models.Model):
    pinned_photo = models.ForeignKey(to=Photo, on_delete=models.CASCADE, related_name="pinned_photos", null=True, blank=True)
