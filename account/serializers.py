from rest_framework import serializers
from account.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'Name', 'password', 'password2', 'tc']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and confirm password don't match")
        return attrs

    def create(self, validated_data):
        # Remove 'password2' from validated_data before calling create_user
        password2 = validated_data.pop('password2', None)

        # Create the user using create_user method
        user = User.objects.create_user(**validated_data)

        return user
    

class UserLoginSerializer (serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    password= serializers.CharField(max_length=255)
    class Meta:
        model=User
        fields=['email','password']

class UserProfileSerializer (serializers.ModelSerializer):
    # email=serializers.EmailField(max_length=255)
    # password= serializers.CharField(max_length=255)
    class Meta:
        model=User
        fields=['id','email','Name']

class UserchangePasswordSerializer(serializers.Serializer):
    password= serializers.CharField(max_length=255, style={'input_type':'password'},write_only=True)
    password2= serializers.CharField(max_length=255, style={'input_type':'password'},write_only=True)
    class Meta:
        fields= ['password','password2']

    def validate(self, attrs):
        password= attrs.get('password')
        password2= attrs.get('password2')
        user=self.context.get('user')
        if password!= password2:
            raise serializers.DjangoValidationError("password and confirm password dosent match")
        # return super().validate(attrs)
    
        user.set_password(password)
        user.save()
        return attrs