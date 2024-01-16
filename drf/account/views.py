import random
from utils import send_otp_code
from .models import OtpCode, User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView
from .serializers import UserRegisterSerializer, OtpCodeSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
import json

class UserRegisterView(APIView):
    """
        Method: POST \n
            Use for user registration \n
        inputs: \n
            - phone_number: 11 digits \n
            - email: at least 6 chars. max 255 chars \n
            - full_name: max 255 chars \n
            - password: at least 6 chars \n
            - password2: at least 6 chars. must be exact password \n
        return: \n
            - success: True if user created successfully (201), then should be redirected to verify url. Otherwise return errors list (400). \n
    """
    serializer_class = UserRegisterSerializer

    def post(self, request):
        ser_data = UserRegisterSerializer(data=request.POST)
        if ser_data.is_valid():
            random_code = random.randint(1000, 9999)
            send_otp_code(ser_data.validated_data['phone_number'], random_code)
            ser_OtpCode = OtpCodeSerializer(data={'code': random_code,
                                                  'phone_number': ser_data.validated_data['phone_number']})
            if ser_OtpCode.is_valid():
                ser_OtpCode.save()
            request.session['user_registration_info'] = {
                # 'ser_data': ser_data,
                'phone_number': ser_data.validated_data['phone_number'],
                'email': ser_data.validated_data['email'],
                'full_name': ser_data.validated_data['full_name'],
                'password': ser_data.validated_data['password'],
                'password2': ser_data.validated_data['password2'],
            }
            # ser_data.create(ser_data.validated_data)
            return Response({'success': True}, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

class UserRegisterVerifyCodeView(APIView):
    """
        Method: POST \n
            Use for confirm otp code \n
        input: \n
            - code: inserted otp code form user. 4 digits \n
        return: \n
            - success: True if user created successfully (201). Otherwise False (400). \n
    """
    serializer_class = OtpCodeSerializer
    def post(self, request, *args, **kwargs):
        user_session = request.session['user_registration_info']
        code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        form = OtpCodeSerializer(data=request.POST, partial=True)
        if form.is_valid():
            cd = form.validated_data
            if cd['code'] == code_instance.code:
                ser_user = UserRegisterSerializer(data=user_session, partial=True)
                print(ser_user)
                if ser_user.is_valid():
                    ser_user.create(ser_user.validated_data)
                    return Response({'success': True}, status=status.HTTP_201_CREATED)
        return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    """
        Method: GET \n
            Use for user logout \n
            - User must be logged in before this. \n
        return: \n
            - success: True if user successfully logged out (200). Otherwise False (400). \n
    """

    def get(self, request, *args, **kwargs):
        if request.user:
            logout(request)
            return Response({'success': True}, status=status.HTTP_200_OK)
        return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)

class VerifyPassword(APIView):
    """
        Method: POST \n
            Use for user login \n
        input: \n
            - phone_number: 11 digits \n
            - password: at least 6 chars \n
        return: \n
            - success: True if user successfully logged in (200). Otherwise False(401). \n
    """
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')
        user = authenticate(request, phone_number=phone_number, password=password)
        if user:
            login(request, user)
            return Response({'success': True}, status=status.HTTP_200_OK)
        return Response({'success': False}, status=status.HTTP_401_UNAUTHORIZED)


class UserCheckLoginPhone(APIView): # NEW
    """
        Method: POST \n
            use to check entered phone number existence in db.
        Input: \n
            - phone_number: 11 digits \n
        return: \n
            - newUser: True if this phone number doesn't found in db. False if phone number found in db.
    """
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phoneNumber')

        try:
            user = User.objects.get(phone_number=phone_number)
            # User with this phone number already exists
            return Response({'newUser': False, 'message': 'User with this phone number already exists'}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'newUser': True, 'message': 'Phone number is New'}, status=status.HTTP_200_OK)

class GenerateOTP(APIView):
    """
    Method: POST \n
        Use to generate and send OTP to the provided phone number. \n
    Input: \n
        - phone_number: 11 digits \n
    Return: \n
        - success: True if OTP is sent successfully \n
        - message: Informational message \n
    """
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phoneNumber')
        # Generate a random 6-digit OTP
        otp_code = ''.join([str(random.randint(0, 9)) for _ in range(5)])
        print(otp_code)
        # Save the OTP in your backend (e.g., in a model or cache)
        ser_OtpCode = OtpCodeSerializer(data={'code': int(otp_code),
                                              'phone_number': phone_number})
        if ser_OtpCode.is_valid() and not OtpCode.objects.filter(code= int(otp_code),phone_number= phone_number).exists():
            ser_OtpCode.save()
        # Send the OTP to the user (you can use an SMS gateway or any other method)
        # TODO
        # send_otp_code(phone_number, otp_code)
        return Response({'success': True, 'message': 'OTP sent successfully'}, status=status.HTTP_200_OK)

class VerifyOTP(APIView):
    """
    Method: POST
        Use to verify the entered OTP and proceed to registration.
    Input:
        - phone_number: 11 digits
        - otp: 6-digit OTP
    Return:
        - success: True if OTP is valid, False otherwise
        - message: Informational message
    """
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))
        phone_number = data.get('phone_number')
        entered_otp = data.get('otp')
        ser_data = UserRegisterSerializer(data=data)

        try:
            user_otp = OtpCode.objects.get(phone_number=phone_number, code=entered_otp)
            # TODO: Register new user with this phone number
            if ser_data.is_valid():
                ser_data.create(ser_data.validated_data)
                user = authenticate(request, phone_number=phone_number, code=entered_otp)
                if user:
                    login(request, user)
            else:
                print(ser_data.errors)
            # OTP is valid, you can proceed to registration
            return Response({'success': True, 'message': 'OTP verified successfully'}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            del ser_data
            return Response({'success': False, 'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
