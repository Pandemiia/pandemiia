from rest_framework import serializers
from rest_framework.serializers import (
    ModelSerializer, StringRelatedField,
    PrimaryKeyRelatedField, SerializerMethodField,
    Serializer, RelatedField
)
from .models import (
    HospitalNeed, Hospital,
    HospitalCategory, Contact,
    Solution, SolutionCategory,
    Tool, Material, SolutionImage
)


class ContactSerializer(ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'full_name', 'position', 'phone', 'email')


class HospitalCategorySerializer(ModelSerializer):
    related_points_number = SerializerMethodField()

    class Meta:
        model = HospitalCategory
        fields = ('id', 'name', 'related_points_number')

    def get_related_points_number(self, category_object) -> int:  # for proper swagger  model
        return category_object.pointmodel_set.count()


class HospitalShortSerializer(ModelSerializer):
    categories = HospitalCategorySerializer(read_only=True, many=True)

    class Meta:
        model = Hospital
        fields = ('id', 'name', 'region', 'categories')

    def get_region(self, obj):
        return obj.get_region_display()


class HospitalSerializer(HospitalShortSerializer):
    contacts = ContactSerializer(read_only=True, many=True)

    class Meta:
        model = Hospital
        fields = (
            'id', 'name', 'description',
            'categories', 'contacts', 'company_code',
            'email', 'region',
        )

    def get_region(self, obj):
        return obj.get_region_display()

    def to_representation(self, instance):
        data = super().to_representation(instance)

        a = {'address': {
              'region': self.get_region(instance),
              'city': instance.city,
              'zipCode': instance.zip_code,
              'line1': instance.line1,
              'geoPosition': {
                  'lat': instance.geo_lat,
                  'lng': instance.geo_lng
              }
          }}
        data.update(a)
        return data


class HospitalDetailedSerializer(HospitalSerializer):
    class Meta:
        model = Hospital
        fields = (
            'id', 'name', 'description',
            'categories', 'contacts', 'company_code',
            'email', 'region',
        )


class SolutionCategorySerializer(ModelSerializer):
    class Meta:
        model = SolutionCategory
        fields = ('id', 'name')


class SolutionToolsSerializer(ModelSerializer):
    class Meta:
        model = Tool
        fields = ('id', 'name',)


class SolutionMaterialsSerializer(ModelSerializer):
    class Meta:
        model= Material
        fields = ('id', 'name',)


class SolutionImagesSerializer(ModelSerializer):
    class Meta:
        model = SolutionImage
        fields = ('id', 'image',)


class SolutionSerializer(ModelSerializer):
    categories = SolutionCategorySerializer(read_only=True, many=True)
    tools = SolutionToolsSerializer(read_only=True, many=True)
    materials = SolutionMaterialsSerializer(read_only=True, many=True)
    images = SolutionImagesSerializer(read_only=True, many=True)

    class Meta:
        model = Solution
        fields = (
            'code', 'name', 'need_description', 'definition',
            'categories', 'main_image', 'attachment', 'instruction',
            'materials', 'tools', 'approved_by', 'images'
        )


class HospitalNeedSerializer(ModelSerializer):
    solution = SolutionSerializer()
    units = SerializerMethodField()

    class Meta:
        model = HospitalNeed
        fields = ('id', 'hospital', 'solution', 'units', 'quantity_needed', 'quantity_received')

    def get_units(self, obj):
        return obj.get_units_display()

    def to_representation(self, instance):
        data = super(HospitalNeedSerializer, self).to_representation(instance)
        q = {'quantity': {
           'needed': instance.quantity_needed,
           'done': instance.quantity_received,
        }}
        data.update(q)
        return data
