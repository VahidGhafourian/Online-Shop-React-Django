from django.core.cache import cache
from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from utils import generate_otp, send_otp_code

from .models import Address, User
from .serializers import AddressSerializer, UserSerializer


# TODO: Fix bugs in add new address with default=True.
class UserCheckLoginPhone(APIView):
    """
    Method: POST \n
        Check entered phone number existence in db and have password or not. \n
    Input: \n
        - phone_number: 11 digits \n
    return: \n
        - newUser: True if this phone number doesn't found in db. False if phone number found in db. \n
        - havePass: True if the user already have password. False if user doesn't set password. \n
    """

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get("phone_number")
        if not phone_number:
            return Response(
                {"error": "Phone number is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
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

        return Response(
            {"new_user": new_user, "have_pass": have_pass}, status=status.HTTP_200_OK
        )


class GenerateSendOTP(APIView):
    """
    Method: POST \n
        - Generate and send OTP to the provided phone number.\n
    Input: \n
        - phone_number: 11 digits \n
    Return: \n
        - success: True if OTP is sent successfully \n
        - message: Informational message \n
    """

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get("phone_number")

        validation_response = self.validate_phone_number(phone_number)
        if validation_response:
            return validation_response
        
        try:
            otp_code = generate_otp()
            self.save_otp(phone_number, otp_code)
            # self.send_otp(phone_number, otp_code) # uncomment in production

            return Response(
                {
                    "success": True,
                    "otp_code": otp_code,
                    "message": "OTP sent successfully",
                },
                status=status.HTTP_200_OK,
            )

        except ValidationError as e:
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return Response(
                {"success": False, "message": f"An unexpected error occurred {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
            
    def validate_phone_number(self, phone_number):
        """
        Validates the phone number. Returns a Response if invalid, otherwise None.
        """
        if not phone_number:
            return Response(
                {"success": False, "message": "Phone number is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not phone_number.isdigit() or len(phone_number) != 11:
            return Response(
                {"success": False, "message": "Phone number must be 11 digits."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return None
        
    def save_otp(self, phone_number, otp_code):
        cache_key = f"otp:{phone_number}"
        cache.set(cache_key, otp_code, timeout=300) # 5 minutes expiration

    def send_otp(self, phone_number, otp_code):
        try:
            send_otp_code(phone_number, otp_code)
        except Exception as e:
            raise ValidationError(f"Failed to send OTP. Please try again later. {e}")


class VerifyOTP(APIView):
    """
    Method: POST \n
        Verify the entered OTP and proceed to registration. \n
    Input: \n
        - phone_number: 11 digits \n
        - otp: 5-digit OTP \n
    Return: \n
        - success: True if OTP is valid, False otherwise \n
        - message: Informational message \n
        - access: JWT access token if OTP is valid \n
        - refresh: JWT refresh token if OTP is valid \n
    """

    def post(self, request):
        try:
            phone_number = request.data.get("phone_number")
            entered_otp = request.data.get("otp")

            self.validate_input(phone_number, entered_otp)
            self.verify_otp(phone_number, entered_otp)
            user = self.get_or_create_user(request.data)
            user.last_login = timezone.now()
            user.save()

            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "success": True,
                    "message": "OTP verified successfully",
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
                status=status.HTTP_200_OK,
            )

        except ValidationError as e:
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"success": False, "message": f"An unexpected error occurred. {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def validate_input(self, phone_number, entered_otp):
        if not phone_number or not entered_otp:
            raise ValidationError("Phone number and OTP are required.")
        if not phone_number.isdigit() or len(phone_number) != 11:
            raise ValidationError("Invalid phone number format.")
        if not entered_otp.isdigit() or len(entered_otp) != 5:
            raise ValidationError("Invalid OTP format.")

    def verify_otp(self, phone_number, entered_otp):
        cache_key = f"otp:{phone_number}"
        otp = cache.get(cache_key)

        if not otp or otp != entered_otp:
            raise ValidationError("Invalid or expired OTP.")
        
        # Delete OTP from Redis after successful verification
        cache.delete(cache_key)

    def get_or_create_user(self, data):
        user, _ = User.objects.get_or_create(phone_number=data.get("phone_number"))
        return user


class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Method: Get \n
            The Current Registred user information \n
        Input: \n
            - \n
        Return: \n
            - The Current Registred user information \n
        """
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Method: POST \n
            Use to set or update the password for the authenticated user. \n
        Input: \n
            - password: New password \n
            - confirm_password: Confirmation of the new password \n
        Return: \n
            - success: True if the password was updated successfully \n
            - message: Informational message \n
        """
        user = request.user
        data = request.data
        user_serializer = UserSerializer(instance=user, data=data, partial=True)

        if user_serializer.is_valid():
            # Save the user with the new password
            user = user_serializer.save()

            return Response(
                {"success": True, "message": "User updated successfully"},
                status=status.HTTP_200_OK,
            )
        else:
            # Return validation errors
            return Response(
                {
                    "success": False,
                    "message": "User update failed",
                    "errors": user_serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

# TODO: Add confirm email view.


class AddressView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Method: GET \n
          - Retrieve all addresses of the authenticated user\n
        Input: \n
            - \n
        Return: \n
            -  \n
        """
        addresses = Address.objects.filter(user=request.user)
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Method: POST \n
            Add new address for user \n
        Input: \n
            - Address information: 'is_default', 'country', 'state', 'city', 'street', 'postal_code' \n
        Return: \n
            - Created Address information. Or Bad Request for invalid data \n
        """
        data = request.data.copy()
        data["user"] = request.user.id
        serializer = AddressSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
