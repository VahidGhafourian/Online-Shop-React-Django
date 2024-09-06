import random
from utils import send_otp_code
from .models import OtpCode, User, Address
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView
from .serializers import UserRegisterSerializer, OtpCodeSerializer, AddressSerializer
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

import json


# class UserLogoutView(APIView):
#     permission_classes = [IsAuthenticated]
#     """
#         Method: POST \n
#             Use for user logout \n
#             - User must be logged in before this. \n
#         return: \n
#             - success: True if user successfully logged out (200). Otherwise False (400). \n
#     """

#     def post(self, request, *args, **kwargs):
#         if request.user:
#             logout(request)
#             return Response({'success': True}, status=status.HTTP_200_OK)
#         return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)

class UserCheckLoginPhone(APIView): # NEW
    """
        Method: POST \n
            use to check entered phone number existence in db and have password or not.
        Input: \n
            - phoneNumber: 11 digits \n
        return: \n
            - newUser: True if this phone number doesn't found in db. False if phone number found in db.
            - havePass: True if the user already have password. False if user doesn't set password.
    """
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phoneNumber')
        if not phone_number:
            return Response({'error': 'Phone number is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(phone_number=phone_number)
            if user.password:
                have_pass = True
            else:
                have_pass = False
            new_user = False
        except User.DoesNotExist:
            have_pass = False
            new_user = True

        return Response({'newUser': new_user, 'havePass': have_pass}, status=status.HTTP_200_OK)

class GenerateSendOTP(APIView):
    """
    Method: POST \n
        Use to generate and send OTP to the provided phone number.\n
    Input: \n
        - phone_number: 11 digits \n
    Return: \n
        - success: True if OTP is sent successfully \n
        - message: Informational message \n
    """
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phoneNumber')
        print(phone_number)
        # Generate a random 6-digit OTP
        otp_code = ''.join([str(random.randint(0, 9)) for _ in range(5)])

        # Save the OTP in your backend (e.g., in a model or cache)
        ser_OtpCode = OtpCodeSerializer(data={'code': otp_code,
                                              'phone_number': phone_number})
        OtpCode.objects.filter(phone_number= phone_number).delete()
        if ser_OtpCode.is_valid():
            ser_OtpCode.save()
            print(otp_code)
            # Send the OTP to the user (you can use an SMS gateway or any other method)
            # TODO
            # send_otp_code(phone_number, otp_code)
            return Response({'success': True, 'otp_code': otp_code, 'message': 'OTP sent successfully'}, status=status.HTTP_200_OK)
        else:
            # print(ser_OtpCode.errors)
            return Response({'success': False, 'message': ser_OtpCode.errors}, status=status.HTTP_400_BAD_REQUEST)



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
        - access: JWT access token if OTP is valid
        - refresh: JWT refresh token if OTP is valid
    """
    def post(self, request, *args, **kwargs):
        data = request.data
        phone_number = data.get('phone_number')
        entered_otp = data.get('otp')
        if OtpCode.objects.filter(phone_number=phone_number, code=entered_otp).exists():

            user_exists = User.objects.filter(phone_number=phone_number).exists()
            if user_exists:
                user = User.objects.get(phone_number=phone_number)
            else:
                user_serializer = UserRegisterSerializer(data={**data, 'phone_number': phone_number})
                if user_serializer.is_valid():
                    user = user_serializer.save()
                else:
                    # print(user_serializer.errors)
                    return Response({'success': False, 'message': 'Cannot Create new user.'},
                                    status=status.HTTP_400_BAD_REQUEST)

                # Generate tokens for the registered user
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            return Response({
                'success': True,
                'message': 'OTP verified successfully',
                'access': access_token,
                'refresh': refresh_token,
                }, status=status.HTTP_200_OK)


        else:
            # print(f"Can't find the {entered_otp=} with {phone_number=}")
            return Response({'success': False, 'message': 'Invalid OTP'},
                            status=status.HTTP_400_BAD_REQUEST)

class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    """
    Method: Get
        The Current Registred user information
    Input:
        -
    Return:
        - The Current Registred user information
    """
    def get(self, request):
        user = request.user
        serializer = UserRegisterSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    """
    Method: POST
        Use to set or update the password for the authenticated user.
    Input:
        - password: New password
        - confirm_password: Confirmation of the new password
    Return:
        - success: True if the password was updated successfully
        - message: Informational message
    """
    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        user_serializer = UserRegisterSerializer(instance=user, data=data, partial=True)

        if user_serializer.is_valid():
            # Save the user with the new password
            user = user_serializer.save()

            return Response({
                'success': True,
                'message': 'Password updated successfully'
            }, status=status.HTTP_200_OK)
        else:
            # Return validation errors
            return Response({
                'success': False,
                'message': 'Password update failed',
                'errors': user_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

class AddressView(APIView):
    permission_classes = [IsAuthenticated]

    """
    Method: GET

    Input:
        -
    Return:
        - Retrieve all addresses of the authenticated user
    """
    def get(self, request, *args, **kwargs):
        addresses = Address.objects.filter(user=request.user)
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    """
    Method: POST
        Add new address for user
    Input:
        - Address information: 'is_default', 'country', 'state', 'city', 'street', 'postal_code'
    Return:
        - Created Address information. Or Bad Request for invalid data
    """
    def post(self, request, *args, **kwargs):
        data = request.data.dict()
        data['user'] = request.user.id
        serializer = AddressSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
