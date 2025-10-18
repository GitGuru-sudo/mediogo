from rest_framework import serializers
from .models import Patient, Helper, Request


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'patient_id', 'name']


class HelperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Helper
        fields = ['id', 'helper_id', 'name', 'phone_number']


class RequestSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    helper_name = serializers.CharField(source='helper.name', read_only=True)
    helper_phone = serializers.CharField(source='helper.phone_number', read_only=True)
    
    class Meta:
        model = Request
        fields = ['id', 'patient', 'patient_name', 'helper', 'helper_name', 
                  'helper_phone', 'floor', 'time_to_reach', 'is_accepted', 'created_at']
        read_only_fields = ['created_at']