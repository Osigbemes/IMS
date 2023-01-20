from decimal import Decimal
from email.policy import default
from rest_framework import serializers
from .models import User, Appointment, Comment

class UserSerializer(serializers.ModelSerializer):
    USERSTATUS=(
            ('DR', 'DOCTOR'),
            ('PR', 'PATIENT')
        )

    password = serializers.CharField(min_length=8, write_only=True)
    userStatus = serializers.ChoiceField(choices=USERSTATUS)

    class Meta:
        model = User
        fields = ('email', 'password', 'username', 'userStatus')
        extra_kwargs = {'password': {'write_only':True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        status = validated_data.pop('userStatus', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        instance.is_active=True
        instance.userStatus=status
        instance.save()
        return instance

class BookAppointment(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ('patientId', 'doctorId', 'date', 'diagnosis')