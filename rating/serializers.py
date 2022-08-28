from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')
    product = serializers.ReadOnlyField(source='product.title')
    class Meta:
        model = Review
        fields = ('__all__')

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        product = self.context.get('product')
        validated_data['user'] = user
        validated_data['product'] = product
        return super().create(validated_data)