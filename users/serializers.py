from rest_framework import serializers
from .models import User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','name','email','password','ride_id',"is_traveler",'is_traveler_companion',"phone_number",'traveler_id',"end_location"]
        #,"is_admin",'is_traveler_companion','traveler_id'
        # ,"is_admin",'is_traveler_companion'
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def create(self,validated_data):
        password = validated_data.pop("password",None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()

        return instance