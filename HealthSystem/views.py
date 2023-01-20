import requests
# from urllib import request
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework.views import APIView, status
from rest_framework import generics
from .models import User, Appointment, Comment
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, BookAppointment
from rest_framework.permissions import AllowAny, IsAuthenticated


class UserRegistration(generics.CreateAPIView):
    permission_classes=[AllowAny]

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            
            token=RefreshToken.for_user(user).access_token
            user.token = token
            user.save()
            
            #user already has a bank account
            # User.objects.filter(customer=user).update(balance=user.initialDeposit,
            #  bankName = user.accountName, accountNumber=user.accountNumber, accountName=user.accountName)
            
            if user:
                return Response({'success':True, 'message':f'Account created successfully {serializer.data}'}, status=status.HTTP_200_OK)
        return Response({'success':False, 'message':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



class BlacklistTokenUpdateView(APIView):
    # the reason we are blacklisting is that when the user logs out we have to black list the refresh token.
    
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response("You are logged out", status=status.HTTP_408_REQUEST_TIMEOUT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # here we are extending the serializer class by customizing the token.
    @classmethod
    def get_token(cls, user):
        #get the token of the user by overwriting the function in the class
        token = super().get_token(user)
        #Add custom claims
        token['username']=user.username
        token['is_staff']=user.is_staff
        token['is_active']=user.is_active
        return token

class Login(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class BookAppointment(generics.CreateAPIView):
    permission_classes = [AllowAny]
    
    serializer_class = BookAppointment
    queryset = Appointment

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            appointment = serializer.save()

            if appointment:
                return Response({'success':True, 'message':f'Appointment booked successfully {serializer.data}'}, status=status.HTTP_200_OK)
        return Response({'success':False, 'message':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class GetPatientVitals(APIView):
    pass