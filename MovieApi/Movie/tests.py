from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory,force_authenticate,APITestCase
from .models import Movies
from .views import MoviesList,MoviesDetail
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
# Create your tests here.

User = get_user_model()

class MovieDetailTestCase(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = AccessToken.for_user(self.user)
        self.mv = Movies.objects.create(
            title="Test Note",
            genre="some test",
            release_date="2023-07-06",
            director="test"
        )
        self.url = f"/api/movies/{self.mv.pk}/"
        self.url1 = f"/api/movies/"

    def test_get_movie(self):
        request = self.factory.get(self.url)
        force_authenticate(request, user=self.user, token=self.token)
        view = MoviesDetail.as_view()
        response = view(request, pk=self.mv.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "success")
        self.assertEqual(response.data["data"]["Movie"]["title"], "Test Note")

    # def test_get_nonexistent_mv(self):
    #     request = self.factory.get("/api/mv/999/")
    #     force_authenticate(request, user=self.user, token=self.token)
    #     view = MvDetail.as_view()
    #     response = view(request, pk=999)
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    #     self.assertEqual(response.data["status"], "fail")
    #     self.assertEqual(response.data["message"], "Note with Id: 999 not found")

    def test_patch_movie(self):
        request = self.factory.patch(self.url, data={"title": "Updated Note"})
        force_authenticate(request, user=self.user, token=self.token)
        view = MoviesDetail.as_view()
        response = view(request, pk=self.mv.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "success")
        self.assertEqual(response.data["data"]["Movie"]["title"], "Updated Note")

    # def test_patch_nonexistent_mv(self):
    #     request = self.factory.patch("/api/mv/999/", data={"title": "Updated Note"})
    #     force_authenticate(request, user=self.user, token=self.token)
    #     view = MvDetail.as_view()
    #     response = view(request, pk=999)
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    #     self.assertEqual(response.data["status"], "fail")
    #     self.assertEqual(response.data["message"], "Note with Id: 999 not found")

    def test_delete_movie(self):
        request = self.factory.delete(self.url)
        force_authenticate(request, user=self.user, token=self.token)
        view = MoviesDetail.as_view()
        response = view(request, pk=self.mv.pk)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Movies.objects.filter(pk=self.mv.pk).exists())

    # def test_delete_nonexistent_mv(self):
    #     request = self.factory.delete("/api/mv/999/")
    #     force_authenticate(request, user=self.user, token=self.token)
    #     view = MvDetail.as_view()
    #     response = view(request, pk=999)
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    #     self.assertEqual(response.data["status"], "fail")
    #     self.assertEqual(response.data["message"], "Note with Id: 999 not found")
    
    def test_movielist_api(self):
        request = self.factory.get(self.url1)
        force_authenticate(request,user=self.user,token=self.token)
        view = MoviesList.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_movie_post_api(self):
        request = self.factory.post(self.url1,data={"title":"Test title","genre":"test","release_date":"2023-07-07","director":"test"})
        force_authenticate(request,user=self.user,token=self.token)
        view= MoviesList.as_view()
        response = view(request)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"],"success")        
