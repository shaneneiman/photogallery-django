# Imports 
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from PIL import Image
from django.shortcuts import get_object_or_404

# Local File Imports
from .serializers import GallerySerializer
from photogallery.models import Gallery, Photo

# Views
class GalleryListCreateView(generics.ListCreateAPIView):
    serializer_class = GallerySerializer

    def get_queryset(self):
        return Gallery.objects.all()

    def perform_create(self, serializer):
        gallery = serializer.save()
        gallery.gallery_of.add(self.request.user)
        

    #def create(self, request, *args, **kwargs):
    #    serializer = self.get_serializer(data=request.data)
    #    serializer.is_valid(raise_exception=True)
    #    self.perform_create(serializer)
    #    self.request.user.gallery_users.add(serializer)
    #    headers = self.get_success_headers(serializer.data)
    #    return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        

class GalleryDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = GallerySerializer

    def get_queryset(self):
        return self.request.user.gallery_users

# Class to restrict file uploads to just images uploads
class ImageUploadParser(FileUploadParser):
    media_type = "image/*"


class PhotoUploadView(APIView):
    parser_classes = (ImageUploadParser, )

    def put(self, request, pk):
        gallery = get_object_or_404(Gallery, pk=pk)
        if 'file' not in request.data:
            raise ParseError("Empty content")

        file = request.data['file']

        try:
            img =Image.open(file)
            img.verify()
        except:
            raise ParseError("Unsupported image type")
        
        photo = Photo.photo.save(file.name, file, commit=False)
        photo.photo_by = request.user
        photo.save()
        gallery.photos.add(photo)
        gallery.save()
        return Response(status=status.HTTP_200_OK)