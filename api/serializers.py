from rest_framework import serializers
from .models import ShellModel

class ShellSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShellModel
        fields = '__all__'