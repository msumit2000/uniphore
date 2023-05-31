from rest_framework import serializers
from .models import MyModel

class corpus(serializers.ModelSerializer):
      class meta:
            model = MyModel
            fields = '__all__'

