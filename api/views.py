# Imports 
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from PIL import Image
from django.shortcuts import get_object_or_404

# Local File Imports
from .serializers import GallerySerializer, PhotoSerializer, NestedCommentSerializer
from photogallery.models import Gallery, Photo, Comment

# Views
#Gallery Views

class GalleryListCreateView(generics.ListCreateAPIView):
    serializer_class = GallerySerializer

    def get_queryset(self):
        return Gallery.objects.for_user(self.request.user)

    def perform_create(self, serializer):
        gallery = serializer.save()
        gallery.gallery_of.add(self.request.user)
        

class GalleryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GallerySerializer

    def get_queryset(self):
        return Gallery.objects.for_user(self.request.user)


#Photo Views

class PhotoDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = PhotoSerializer

    def get_queryset(self):
        return Photo.objects.for_user(self.request.user)

# Class to restrict file uploads to just images uploads
class ImageUploadParser(FileUploadParser):
    media_type = "image/*"


# Add Photo a Gallery
class PhotoUploadtoGalleryView(APIView):
    parser_classes = (ImageUploadParser, )

    # POST image file to create the photo and pk 
    # additionally get the gallery pk from the url,
    # using the pk to get the gallery and add the photo after it is created
    def post(self, request, gallery_pk):
        gallery = get_object_or_404(request.user.gallery_users, pk=gallery_pk)
        if 'file' not in request.data:
            raise ParseError("Empty content")

        file = request.data['file']

        try:
            img = Image.open(file)
            img.verify()
        except:
            raise ParseError("Unsupported image type")
        
        photo = Photo.photo.save(file.name, file, save=False)
        photo.photo_by = request.user
        photo.save()
        gallery.photos.add(uploaded_photo)
        return Response(status=status.HTTP_201_CREATED)
    
    # PUT additional information or edit the photo using the pk
    def put(self, request, photo_pk):
        photo = get_object_or_404(request.user.user_photos, pk=photo_pk)
        serializer = PhotoSerializer(photo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE the photo using the pk, after removing it from the Gallery
    def delete(self, request, gallery_pk, photo_pk):
        gallery = get_object_or_404(request.user.gallery_users, pk=gallery_pk)
        photo = get_object_or_404(request.user.user_photos, pk=photo_pk)
        gallery.photos.remove(photo)
        photo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Add Photo with no relation to a Gallery
class PhotoUploadView(APIView):
    parser_classes = (ImageUploadParser, )

    # POST the image file resulting in the creating of the photo and pk
    def post(self, request):
        if 'file' not in request.data:
            raise ParseError("Empty content")

        file = request.data['file']

        try:
            img = Image.open(file)
            img.verify()
        except:
            raise ParseError("Unsupported image type")

        photo = Photo.photo.save(file.name, file, save=False)
        photo.photo_by = request.user
        photo.save()
        return Response(status=status.HTTP_201_CREATED)

    # PUT additional information or edit the photo using the pk
    def put(self, request, pk):
        photo = get_object_or_404(request.user.user_photos, pk=pk)
        serializer = PhotoSerializer(photo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE the photo using the pk
    def delete(self, request, pk):
        photo = get_object_or_404(request.user.user_photos, pk=pk)
        photo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
