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
from photogallery.models import Gallery

# Views
class GalleryListCreateView(generics.ListCreateAPIView):
    serializer_class = GallerySerializer

    def get_queryset(self):
        return Gallery.objects.all()

    def perform_create(self, serializer):
        serializer.save(gallery_of.add(request.user))
        #serializer.gallery_of.add(request.user)
        #serializer.save()

class GalleryDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = GallerySerializer

    def get_queryset(self):
        return self.request.user.gallery_users

# Class to restrict file uploads to just images uploads
class ImageUploadParser(FileUploadParser):
    media_type = "image/*"


class PhotoUploadtoGalleryView(APIView):
    parser_classes = (ImageUploadParser)

    def put(self, request, gallery_pk):
        gallery = get_object_or_404(self.request.user.user_galleries, pk=gallery_pk)
        if 'file' not in request.data:
            raise ParseError("Empty content")

        file = request.data['file']

        try:
            img =Image.open(file)
            img.verify()
        except:
            raise ParseError("Unsupported image type")
        
        gallery.photos.save(file.name, file, save=True)
        return Response(status=status.HTTP_200_OK)