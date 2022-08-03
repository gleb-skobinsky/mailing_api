from email.policy import default
from rest_framework import serializers
from mailing.models import Mailing, Client, TIMEZONES
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator

class MailingSerializer(serializers.Serializer):
    class Meta:
        model = Mailing
        fields = '__all__'

    time_start = serializers.DateTimeField(required=True)
    message_text = serializers.CharField(required=True, min_length=1, max_length=1024)
    mobile_code = serializers.IntegerField(required=False, allow_null=True, min_value=100, max_value=999)
    tag = serializers.CharField(required=False, allow_null=True, max_length=32)
    time_end = serializers.DateTimeField(required=True)

    def create(self, validated_data):
        return Mailing.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.time_start = validated_data.get("time_start", instance.time_start)
        instance.message_text = validated_data.get("message_text", instance.message_text)
        instance.mobile_code = validated_data.get("mobile_code", instance.mobile_code)
        instance.tag = validated_data.get("tag", instance.tag)
        instance.time_end = validated_data.get("time_end", instance.time_end)
        instance.save()
        return instance

class ClientSerializer(serializers.Serializer):
    class Meta:
        model = Client
        fields = '__all__'

    phone_number = serializers.RegexField(max_length = 11, 
                                        min_length=11, 
                                        regex = r"\b7[0-9]{10}\b", 
                                        required=True, 
                                        validators=[UniqueValidator(queryset=Client.objects.all(),
                                        message=("Phone number already exists"))])
    mobile_code = serializers.IntegerField(min_value=100, max_value = 999, required=True)
    tag = serializers.CharField(max_length=32, required=True)
    timezone = serializers.ChoiceField(choices=TIMEZONES, required=True)

    def create(self, validated_data):
        new_client = Client.objects.create(**validated_data)
        return new_client

    def update(self, instance, validated_data):
        instance.phone_number = validated_data.get("phone_number", instance.phone_number)
        instance.mobile_code = validated_data.get("mobile_code", instance.mobile_code)
        instance.tag = validated_data.get("tag", instance.tag)
        instance.timezone = validated_data.get("timezone", instance.timezone)
        instance.save()
        return instance



