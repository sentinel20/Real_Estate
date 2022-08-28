from multiprocessing import context
from rest_framework import permissions, response, generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from .permissions import IsAuthor
from . import serializers
from .models import Listing, Comment, Like, Favorites
from rest_framework.decorators import action
from rest_framework.response import Response
from rating.serializers import ReviewSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
# Create your views here.

class Pagination(PageNumberPagination):
    page_size = 2
    page_query_param = 'page'
    max_page_size = 1000

class ListingViewSet(ModelViewSet):
    queryset = Listing.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('title','price', 'num_bedrooms', 'num_bathrooms', 'address',)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ListingListSerializer
        return serializers.ListingDetailSerializer

    # api/v1/listings/<id>/reviews/
    @action(['GET', 'POST'], detail=True)
    def rating(self, request, pk=None):
        product = self.get_object()
        if request.method == 'GET':
            reviews = product.reviews.all()
            serializer = ReviewSerializer(reviews, many=True).data
            return response.Response(serializer, status=200)
        data = request.data
        serializer = ReviewSerializer(data=data, context = {'request': request, 'product': product})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data, status=201)

    # api/v1/listings/<id>/comments/
    @action(['GET'], detail=True)
    def comments(self, request, pk):
        product = self.get_object()
        comments = product.comments.all()
        serializer = serializers.CommentSerializer(comments, many=True)
        return Response(serializer.data, status=200)

    # api/v1/listings/<id>/add_to_liked/
    @action(['POST'], detail=True)
    def add_like(self, request, pk):
        product = self.get_object()
        if request.user.liked.filter(product=product).exists():
            request.user.liked.filter(product=product).delete() # способ удаления лайка
            return Response('Liked', status=204)  # нужно написать "вы удалили лайк"
        Like.objects.create(product=product, owner=request.user)
        return Response('Like', status=201)

    # api/v1/listings/<id>/get_likes/
    @action(['GET'], detail=True)
    def get_likes(self, request, pk):
        product = self.get_object()
        likes = product.likes.all()
        serializer = serializers.LikedSerializer(likes, many = True)
        return Response (serializer.data, status=200)

    #  api/v1/listings/<id>/favorites/
    @action(['POST'], detail=True)
    def favorites(self, request, pk):
        product = self.get_object()
        if request.user.favorites.filter(product=product).exists():
            request.user.favorites.filter(product=product).delete()
            return Response('Delete from favorites!', status=204)
        Favorites.objects.create(product=product, owner=request.user)
        return Response('Added to favorites!', status=201)

class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthor,)