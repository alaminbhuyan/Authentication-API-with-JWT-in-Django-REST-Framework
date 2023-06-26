from rest_framework import serializers
from account.models import MyUser
# ================== For Email sending =================
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from account.utils import SendEmail


# User Registration Serializer class
class UserRegistrationSerializer(serializers.ModelSerializer):
    # we are writing this because we need confirm password field in our registration request
    password2 = serializers.CharField(
        style={"input_type": "password"}, write_only=True)

    class Meta:
        model = MyUser
        fields = ["username", "first_name", "last_name", "email",
                  "password", "password2", "terms_and_condition"]
        extra_kwargs = {"password": {"write_only": True}}

    # Validating Password and Confirm Password while Registration
    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")

        if password != password2:
            raise serializers.ValidationError(
                "Password and Confirm Password do not match")

        return attrs

    # create a user
    def create(self, validated_data):
        return MyUser.objects.create_user(**validated_data)

# User Login Serializer class


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = MyUser
        fields = ['email', 'password']


# User Profile Serializer class
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'username', 'first_name',
                  'last_name', 'email', 'terms_and_condition']


# User Change Password Serializer class
class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError(
                "Password and Confirm Password do not match")

        user.set_password(password)
        user.save()
        return attrs


# Send password reset email serializer class
class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if MyUser.objects.filter(email=email).exists():
            user = MyUser.objects.get(email=email)
            user_id = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user=user)
            generated_link = "http://localhost:3000/api/reset/" + user_id + "/" + token
            print(generated_link)
            # Sending email
            body = "Click here to reset your password: " + generated_link
            data = {
                "subject": "Reset Your Password",
                "body": body,
                "to_email": user.email
            }
            SendEmail.send_email(data=data)
            return attrs
        else:
            raise serializers.ValidationError("You are not Registered User")


# User password reset email serializer class
class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            user_id = self.context.get('user_id')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError(
                    "Password and Confirm Password doesn't match")
            id = smart_str(urlsafe_base64_decode(user_id))
            user = MyUser.objects.get(id=id)
            # Checking if user token is valid or exist or not
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError(
                    'Token is not Valid or Expired')
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError('Token is not Valid or Expired')
