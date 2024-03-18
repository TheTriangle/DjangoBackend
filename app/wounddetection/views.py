from django.contrib.auth import login
from django.shortcuts import render

from rest_framework import permissions, status, generics, viewsets
from rest_framework import views
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from .models import WoundReport, Patient, Case, Doctor
from .serializers import PatientSerializer, DoctorSerializer


class CasesView(generics.ListCreateAPIView):
    serializer_class = serializers.CaseSerializer
    queryset = Case.objects.all()
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class WoundUploadView(generics.ListCreateAPIView):

    serializer_class = serializers.WoundReportSerializer
    queryset = WoundReport.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PatientView(generics.CreateAPIView):
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs["context"] = self.get_serializer_context()

        # Check if a pk was passed through the url.
        if 'pk' in self.kwargs:
            modified_data = self.request.data.copy()
            modified_data['school'] = self.kwargs.get('pk')
            kwargs["data"] = modified_data
            return serializer_class(*args, **kwargs)

        # If not mind, move on.
        return serializer_class(*args, **kwargs)


class DoctorView(APIView):
    def get(self, request, pk):
        try:
            doctor = Doctor.objects.get(pk=pk)
        except Doctor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = DoctorSerializer(doctor)
        return Response(serializer.data)

    def post(self, request, pk):
        try:
            doctor = Doctor.objects.get(pk=pk)
            serializer = DoctorSerializer(doctor, data=request.data)
        except Doctor.DoesNotExist:
            serializer = DoctorSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(generics.RetrieveAPIView):
    serializer_class = serializers.UserSerializer

    def get_object(self):
        return self.request.user


class LoginView(views.APIView):
    # This view should be accessible also for unauthenticated users.
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = serializers.LoginSerializer(data=self.request.data,
                                                 context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(None, status=status.HTTP_202_ACCEPTED)
