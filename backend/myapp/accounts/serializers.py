from rest_framework import serializers

class UserRegisterSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    id_document = serializers.CharField(max_length=15)
    role = serializers.CharField()