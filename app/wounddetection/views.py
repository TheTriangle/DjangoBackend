from django.contrib.auth import login
from pathlib import Path

from rest_framework import permissions, status, generics
from rest_framework import views
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from .model.model import Model
from .models import WoundReport, Patient, Case, Doctor
from .serializers import PatientSerializer, DoctorSerializer


class CasesView(generics.ListCreateAPIView):
    serializer_class = serializers.CasePostSerializer
    queryset = Case.objects.all()

    def perform_create(self, serializer):
        case = serializer.save()

        patient_id = self.request.data.get('patient')

        patient = Patient.objects.get(id=patient_id)

        patient.cases.add(case)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


net = Model()
net.load_model(Path(__file__).parent / r"model/model.pkl")


class WoundUploadView(generics.ListCreateAPIView):

    serializer_class = serializers.WoundReportSerializer
    queryset = WoundReport.objects.all()

    def perform_create(self, serializer):
        report = serializer.save()

        case_id = self.request.data.get('case')

        # Затем находим пациента по ID
        case = Case.objects.get(id=case_id)

        # Добавляем созданный случай к связанным случаям пациента
        case.reports.add(report)

    def create(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        image_url = serializer.data["image_url"]
        path = str(str(Path(__file__).parent) + "\\..\\..\\mediafiles\\" + image_url[image_url.find("images"):])
        stage = net.predict(path)
        serializer.instance.additional = "Stage: " + str(stage)
        serializer.instance.save()
        ans = serializer.data
        ans["additional"] = "Stage: " + str(stage)
        return Response(ans, status=status.HTTP_201_CREATED)


class PatientView(generics.CreateAPIView):
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()


    def get(self, request, pk):
        try:
            patient = Patient.objects.get(pk=pk)
        except Patient.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PatientSerializer(patient)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        # Deserialize the request data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Create a patient instance
        patient_instance = Patient.objects.create(name=serializer.validated_data['name'],
                                                  mail=serializer.validated_data['mail'])

        # Add cases to the patient instance if provided
        if 'cases' in serializer.validated_data:
            patient_instance.cases.set(serializer.validated_data['cases'])

        # Serialize the patient instance and return the response
        serializer = self.get_serializer(patient_instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
