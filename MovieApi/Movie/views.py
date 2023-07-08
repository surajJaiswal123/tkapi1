from django.shortcuts import render
from rest_framework import generics,status
from Movie.models import Movies
from Movie.serializers import MovieSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
# Create your views here.

class CustomPage(PageNumberPagination):
    page_size_query_param = 'page_size'

class MoviesList(generics.GenericAPIView):
    serializer_class = MovieSerializer
    queryset = Movies.objects.all()
    permission_classes = (IsAuthenticated,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['genre', 'director']
    paginator = CustomPage()

    def get(self,request):
        if request.query_params.get('search'):
            movies_data = self.filter_queryset(self.get_queryset())
        else:
            movies_data = Movies.objects.all()
        if request.query_params.get('page_size'):
            self.paginator.page_size = int(request.query_params.get('page_size'))
            paginated_notes = self.paginate_queryset(movies_data)
            serializer = self.serializer_class(paginated_notes, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = self.serializer_class(movies_data, many=True)
            return Response({"count":len(serializer.data),"data":{"Movie":serializer.data}},status=status.HTTP_200_OK)
        
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": {"Movie": serializer.data}},status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "fail", "message": serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        
class MoviesDetail(generics.GenericAPIView):
    serializer_class = MovieSerializer
    def get_movie(self,pk):
        try:
            return Movies.objects.get(pk=pk)
        except:
            return None
    def get(self,request,pk):
        record = self.get_movie(pk=pk)
        if record == None:
            return Response({"status": "fail", "message": f"Movie with Id: {pk} not found"},status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(record)
        return Response({"status": "success", "data": {"Movie": serializer.data}})
    def patch(self, request, pk):
        record = self.get_movie(pk)
        if record == None:
            return Response({"status": "fail", "message": f"Movie with Id: {pk} not found"},status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(record,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": {"Movie": serializer.data}})
        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk):
        record = self.get_movie(pk)
        if record == None:
            return Response({"status": "fail", "message": f"Movie with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)
        record.delete()
        return Response({"status": "success"},status=status.HTTP_204_NO_CONTENT)
