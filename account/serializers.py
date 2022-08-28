from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _
from listing.serializers import FavoritesSerializer

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(min_length=6, max_length=100, required=True, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password2')

    def validate(self, attrs):
        password2 = attrs.pop('password2')
        if attrs.get('password') != password2:
            raise serializers.ValidationError('Passwords did not match!')
        if not attrs.get('password').isalnum():
            raise serializers.ValidationError('Password field must be contain alpha symbols and numbers!')
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    # def to_representation(self, instance):
    #     repr = super().to_representation(instance)
    #     repr['favorites'] = FavoritesSerializer(instance.favorites.all(), many=True).data
    #     return repr

class LoginSerializer(TokenObtainPairSerializer):
    password = serializers.CharField(min_length=6, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.pop('password')
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User not found')
        user = authenticate(email=email, password=password)
        if user and user.is_active:
            refresh = self.get_token(user)
            attrs['refresh'] = str(refresh)
            attrs['access'] = str(refresh.access_token)
        else:
            raise serializers.ValidationError('Invalid password!')
        return attrs
        
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    default_error_messages = {
        'bad_token': _('Token is invalid or expired!')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100, required=True)

class RestorePasswordSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(min_length=6, required=True)
    password2 = serializers.CharField(min_length=6, required=True)

    def validate(self, attrs):
        password2 = attrs.pop('password2')
        if password2 != attrs['password']:
            raise serializers.ValidationError('Password didn\'t match!')
        try:
            user = User.objects.get(activation_code=attrs['code'])
        except User.DoesNotExist:
            serializers.ValidationError('Your code is incorrect!')
        attrs['user'] = user
        return attrs

    def save(self, **kwargs):
        data = self.validated_data
        user = data['user']
        user.set_password(data['password'])
        user.activation_code = ''
        user.save()
        return user