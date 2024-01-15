from django.contrib.auth.mixins import UserPassesTestMixin
from kavenegar import *

def send_otp_code(phone_number, code):
    try:
        api = KavenegarAPI('4670534A4A78314F646B6B6C514542366673773775427A4A565263513937527176677A4966696D39766D673D')
        params = {
            'sender': '10008663',
            'receptor': phone_number,
            'message': f' کد تایید شما{code}',
        }
        response = api.sms_send(params)
        print(response)

    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)

class IsAdminUserMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin
