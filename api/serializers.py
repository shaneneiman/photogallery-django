from rest_framework import serializers
from photogallery.models import Gallery, Photo, Comment

class GallerySerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="gallery_of.get", read_only=True)

    class Meta:
        model = Gallery
        fields = [
            "id",
            "username",
            "title",
            "public_gallery"
        ]

