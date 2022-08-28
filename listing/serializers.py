from rest_framework import serializers
from .models import Listing, Comment, Like, Favorites
from django.db.models import Avg

class ListingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = ('title', 'price', 'image')

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['rating'] = instance.reviews.aggregate(Avg('rating'))['rating__avg']
        return repr

class FavoritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = ('product',)

    def to_representation(self, instance):
        repr =  super().to_representation(instance)
        repr['product'] = ListingListSerializer(instance.product).data
        return repr

class ListingDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = '__all__'

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['rating'] = instance.reviews.aggregate(Avg('rating'))['rating__avg']
        repr['reviews'] = instance.reviews.count()
        return repr 

    def is_liked(self, product):
        user = self.context.get('request').user
        return user.liked.filter(product=product).exists()
    def to_representation(self, instance):    # 2-способ коммент отсветить
        repr = super().to_representation(instance)
        # repr['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        user = self.context.get('request').user
        if user.is_authenticated:
            repr['is_liked'] = self.is_liked(instance)
        repr['likes_count'] = instance.likes.count()
        return repr

class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Comment
        fields = ('id', 'body', 'owner', 'product')

class LikedSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Like
        fields = ('owner',)

