from django.contrib.auth import login
from django.shortcuts import render

from rest_framework import permissions, status, generics, viewsets
from rest_framework import views
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from .models import WoundReport, Patient, Case, Doctor
from .serializers import PatientSerializer, DoctorSerializer, CaseSerializer, WoundReportSerializer


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

    def post(self, request, *args, **kwargs):
        # Deserialize the request data for patient
        patient_serializer = self.get_serializer(data=request.data)
        patient_serializer.is_valid(raise_exception=True)

        # Create patient instance
        patient_instance = Patient.objects.create(name=patient_serializer.validated_data['name'],
                                                   mail=patient_serializer.validated_data['mail'])

        # Deserialize the request data for cases
        case_serializer = CaseSerializer(data=request.data.get('cases', []), many=True)
        case_serializer.is_valid(raise_exception=True)

        # Create case instances and associate with patient
        for case_data in case_serializer.validated_data:
            # Extract reports data from case_data
            reports_data = case_data.pop('reports', [])

            # Create the case instance
            case_instance = Case.objects.create(patient=patient_instance, **case_data)

            # Associate reports with the case using set() method
            woundsSerializer = WoundReportSerializer(data=reports_data, many=True)
            woundsSerializer.is_valid(raise_exception=True)
            wound_instance = WoundReport.objects.create(**woundsSerializer.validated_data, many=True)
            case_instance.reports.set(wound_instance)

        # Serialize the patient instance and return the response
        patient_serializer = self.get_serializer(patient_instance)
        return Response(patient_serializer.data, status=status.HTTP_201_CREATED)


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
