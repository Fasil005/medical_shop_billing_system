from rest_framework import serializers

from users.models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
        depth=0
        extra_kwargs = {
            'password': {'write_only': True},
            'is_superuser': {'write_only': True},
            'last_login': {'write_only': True},
            'is_staff': {'write_only': True},
            'groups': {'write_only': True},
            'permissions': {'write_only': True},
            'user_permissions': {'write_only': True},
            }
    
    def create(self, validated_data):
       
        password = validated_data.pop('password', None)
        user = User(**validated_data)

        if password:
            user.set_password(password)
        user.save()
        
        return user 
