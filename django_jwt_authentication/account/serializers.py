from rest_framework import serializers
from account.models import MyUser


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
            raise serializers.ValidationError("Password and Confirm Password do not match")
        
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
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'terms_and_condition']
