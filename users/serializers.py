from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import CustomUser,CodeVerified,VIA_PHONE,VIA_EMAIL
from shared.utility import chech_email_or_phone_number,send_to_mail

class SignUpSerializer(serializers.ModelSerializer):
    # id = serializers.UUIDField(read_only=True)
    auth_type = serializers.CharField(required=False,read_only=True)
    auth_status = serializers.CharField(required=False,read_only=True)

    def __init__(self,*args,**kwargs):
        super(SignUpSerializer,self).__init__(*args,**kwargs)
        self.fields['email_phone_number'] = serializers.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = ['id','auth_type','auth_status']
        read_only_fields = ('auth_status',)

    def create(self, validated_data):
        user =super(SignUpSerializer,self).create(validated_data)
        if user.auth_type == VIA_EMAIL:
            code = user.create_verify_code(VIA_EMAIL)
            send_to_mail(user.email,code)
        elif user.auth_type == VIA_PHONE:
            code = user.create_verify_code(VIA_PHONE)
            send_to_mail(user.phone,code)
        user.save()
        print(code)
        return user

    def validate(self,data):
        super(SignUpSerializer,self).validate(data)
        data = self.auth_validate(data)
        return data

    def validate_email_phone_number(self,data):
        if data and CustomUser.objects.filter(email = data).exists():
            raise ValidationError("Bu emaildan ruyxatdan utgan")
        elif data and CustomUser.objects.filter(phone = data).exists():
            raise ValidationError("Bu raqamdan ruyxatdan utgan")
        return data

    @staticmethod
    def auth_validate(data):
        user_input = str(data.get('email_phone_number')).lower()
        auth_type = chech_email_or_phone_number(user_input)
        print(user_input)
        if auth_type == 'email':
            data = {
                'auth_type' : VIA_EMAIL,
                'email' : user_input
            }
        elif auth_type == 'phone':
            data = {
                'auth_type' : VIA_PHONE,
                'phone' : user_input
            }
        else:
            data = {
                'succes':False,
                'msg':"Noto'g'ri malumot kiritdingiz"
            }
            raise ValidationError(data)
        return data

    def to_representation(self,instance):
        data = super(SignUpSerializer,self).to_representation(instance)
        data.update(instance.token())
        return data
