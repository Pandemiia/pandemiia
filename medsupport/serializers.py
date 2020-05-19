from django.db.models import Count, Sum
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
    Tool, Material, SolutionImage,
    SolutionType, ApprovedBy
)


class ContactSerializer(ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'full_name', 'position', 'phone', 'email')


class HospitalCategorySerializer(ModelSerializer):
    related_hospitals_number = SerializerMethodField()

    class Meta:
        model = HospitalCategory
        fields = ('id', 'name', 'related_hospitals_number')

    def get_related_hospitals_number(self, category_object) -> int:  # for proper swagger  model
        return category_object.hospital_set.count()


class NeedSolutionTypeSerializer(serializers.ModelSerializer):
    # N.B! annotated fields
    received = serializers.IntegerField(read_only=True)
    needed = serializers.IntegerField(read_only=True)

    class Meta:
        model = SolutionType
        fields = ('id', 'name', 'received', 'needed')


class HospitalSerializer(ModelSerializer):
    categories = HospitalCategorySerializer(read_only=True, many=True)
    need_types = NeedSolutionTypeSerializer(read_only=True, many=True)
    contacts = ContactSerializer(read_only=True, many=True)

    class Meta:
        model = Hospital
        fields = (
            'id', 'name', 'description',
            'categories', 'contacts', 'company_code',
            'email', 'region', 'need_types'
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


class HospitalRegionsSerializer(Serializer):
    key = serializers.IntegerField()
    name = serializers.CharField()
    hospitals_in_region = serializers.IntegerField()


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
        model = Material
        fields = ('id', 'name',)


class SolutionImagesSerializer(ModelSerializer):
    class Meta:
        model = SolutionImage
        fields = ('id', 'image',)


class ApprovedBySerializer(ModelSerializer):
    class Meta:
        model = ApprovedBy
        fields = ('id', 'org_name', 'logo')


class SolutionSerializer(ModelSerializer):
    tools = SolutionToolsSerializer(read_only=True, many=True)
    materials = SolutionMaterialsSerializer(read_only=True, many=True)
    images = SolutionImagesSerializer(read_only=True, many=True)
    solution_type = PrimaryKeyRelatedField(read_only=True)
    approved_by = ApprovedBySerializer(read_only=True)

    class Meta:
        model = Solution
        fields = (
            'solution_type', 'code', 'name', 'need_description', 'definition',
            'manufacturing_options', 'main_image', 'attachment', 'instruction',
            'source', 'materials', 'tools', 'approved_by', 'comment', 'images',
            'source',
        )


class SolutionShortSerializer(ModelSerializer):
    tools = SolutionToolsSerializer(read_only=True, many=True)
    materials = SolutionMaterialsSerializer(read_only=True, many=True)
    solution_type = PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Solution
        fields = (
            'id', 'solution_type', 'code', 'name',
            'main_image', 'attachment',
            'materials', 'tools', 'approved_by',
        )


class SolutionTypeSerializer(ModelSerializer):
    categories = SolutionCategorySerializer(read_only=True, many=True)
    solutions = SolutionShortSerializer(read_only=True, many=True)
    units = SerializerMethodField()

    def get_units(self, obj):
        return obj.get_units_display()

    class Meta:
        model = SolutionType
        fields = ('name', 'categories', 'units', 'solutions')


class HospitalNeedSerializer(ModelSerializer):
    solution_type = SolutionTypeSerializer(read_only=True)

    class Meta:
        model = HospitalNeed
        fields = ('id', 'hospital', 'solution_type', )

    def to_representation(self, instance):
        data = super(HospitalNeedSerializer, self).to_representation(instance)
        q = {'quantity': {
            'needed': instance.quantity_needed,
            'received': instance.quantity_received,
        }}
        data.update(q)
        return data
