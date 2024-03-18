from django.contrib.auth import authenticate

from rest_framework import serializers
from django.contrib.auth.models import User

from .models import WoundReport, Case, Patient, Doctor


class WoundReportSerializer(serializers.ModelSerializer):
    depth = serializers.CharField(
        label="depth"
    )
    category = serializers.CharField(
        label="woundClass"
    )
    type = serializers.CharField(
        label="type"
    )
    area = serializers.CharField(
        label="area"
    )
    diameter = serializers.CharField(
        label="diameter"
    )
    additional = serializers.CharField(
        label="additional"
    )
    image_url = serializers.ImageField(required=False)

    class Meta:
        model = WoundReport
        fields = ['id', 'depth', 'category', 'type', 'area', 'diameter', 'additional', 'image_url']


class CaseSerializer(serializers.ModelSerializer):
    reports = WoundReportSerializer(read_only=True, many=True)

    class Meta:
        model = Case
        fields = ['id', 'doctor', 'reports']

class PatientSerializer(serializers.ModelSerializer):
    cases = CaseSerializer(read_only=True, many=True)

    class Meta:
        model = Patient
        fields = ['cases', 'id', 'name', 'mail']

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]

class LoginSerializer(serializers.ModelSerializer):
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
