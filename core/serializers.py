from rest_framework import serializers
from .models import User, Profile
from django.contrib.auth.hashers import make_password, check_password


# ------------------ PROFILE SERIALIZER ------------------
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['address', 'date_of_birth', 'bio', 'profile_picture']


# ------------------ USER REGISTER SERIALIZER ------------------
class UserRegisterSerializer(serializers.ModelSerializer):
    # Nested profile fields
    profile = ProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'email', 'user_id', 'password', 'profile']

    def create(self, validated_data):
        # Extract profile data if available
        profile_data = validated_data.pop('profile', None)

        # Hash password before saving
        validated_data['password'] = make_password(validated_data['password'])
        user = super().create(validated_data)

        # Create Profile automatically
        if profile_data:
            Profile.objects.create(user=user, **profile_data)
        else:
            Profile.objects.create(user=user)

        return user


# ------------------ LOGIN SERIALIZER ------------------
class UserLoginSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        try:
            user = User.objects.get(user_id=data['user_id'])
        except User.DoesNotExist:
            raise serializers.ValidationError({"message": "User not found"})

        if not check_password(data['password'], user.password):
            raise serializers.ValidationError({"message": "Invalid credentials"})

        return {"message": "Login successful!", "user_id": user.user_id}


# ------------------ PROFILE UPDATE SERIALIZER ------------------
class ProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(source="user.user_id", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    phone = serializers.CharField(source="user.phone", read_only=True)

    class Meta:
        model = Profile
        fields = [
            "user_id", "first_name", "last_name", "email", "phone",
            "address", "date_of_birth", "bio", "profile_picture"
        ]


    def update(self, instance, validated_data):
        # Extract user data
        user_data = validated_data.pop('user', {})

        # Update Profile fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update User fields
        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        return instance
