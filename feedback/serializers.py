from rest_framework import serializers
from .models import Feedback


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ["ride","user",'rating','comment','timestamp']

    def create(self,validated_data):
        
        instance = self.Meta.model(**validated_data)
        instance.save()

        return instance