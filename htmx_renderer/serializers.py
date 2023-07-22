from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField


class CompoundRelatedField(PrimaryKeyRelatedField):

    def to_representation(self, value):
        return {
            'pk': super().to_representation(value),
            '__str__': str(value),
        }

    def to_internal_value(self, data):
        if isinstance(data, dict) and 'pk' in data:
            data = data['pk']
        return super().to_internal_value(data)

    def use_pk_only_optimization(self):
        # We need the whole record object
        return False


class HTMXModelSerializer(ModelSerializer):

    def __init__(self, *args, **kwargs):
        self.serializer_related_field = CompoundRelatedField
        print(self.serializer_related_field)
        super().__init__(*args, **kwargs)
