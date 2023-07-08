from django.urls import path
from Movie.views import MoviesList,MoviesDetail

urlpatterns = [
    path('', MoviesList.as_view()),
    path('<str:pk>', MoviesDetail.as_view())
]
