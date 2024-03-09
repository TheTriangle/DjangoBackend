from django.contrib.auth import authenticate

from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Wound


class WoundSerializer(serializers.Serializer):
    depth = serializers.CharField(
        label="Depth"
    )
    category = serializers.CharField(
        label="Category"
    )
    type = serializers.CharField(
        label="Type"
    )
    area = serializers.CharField(
        label="Area"
    )
    diameter = serializers.CharField(
        label="Diameter"
    )
    additional = serializers.CharField(
        label="Additional"
    )
    image_url = serializers.ImageField(required=False)

    class Meta:
        model = Wound
        fields = ['id', 'depth', 'category', 'type', 'area', 'diameter', 'additional', 'image_url']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]


class LoginSerializer(serializers.Serializer):
    """
    This serializer defines two fields for authentication:
      * username
      * password.
    It will try to authenticate the user with when validated.
    """
    username = serializers.CharField(
        label="Username",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        # This will be used when the DRF browsable API is enabled
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        # Take username and password from request
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            # Try to authenticate the user using Django auth framework.
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                # If we don't have a regular user, raise a ValidationError
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        attrs['user'] = user
        return attrs
