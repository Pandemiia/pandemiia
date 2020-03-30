from rest_framework.serializers import ModelSerializer, StringRelatedField, \
    PrimaryKeyRelatedField, SerializerMethodField
from .models import NeedModel, PointModel, CategoryPointModel, ContactModel, ArticleModel


class CategoryPointSerializer(ModelSerializer):
    class Meta:
        model = CategoryPointModel
        fields = ('name',)


class ContactSerializer(ModelSerializer):
    class Meta:
        model = ContactModel
        fields = ('full_name', 'position', 'phone', 'email')


class PointsSerializer(ModelSerializer):
    category = StringRelatedField(read_only=True, many=True)
    contacts = ContactSerializer(read_only=True, many=True)

    class Meta:
        model = PointModel
        fields = ('id', 'name', 'description', 'category', 'contacts')

    def get_region(self, obj):
        return obj.get_region_display()

    def to_representation(self, instance):
        data = super(PointsSerializer, self).to_representation(instance)

        data['address'] = {
                'region': self.get_region(instance),
                'city': instance.city,
                'zipCode': instance.zip_code,
                'line1': instance.line1,
                'geoPosition': {
                    'lat': instance.geo_lat,
                    'lng': instance.geo_lng
                }
            },
        return data


class PointsShortSerializer(ModelSerializer):
    category = StringRelatedField(read_only=True, many=True)

    class Meta:
        model = PointModel
        fields = ('id', 'name', 'region', 'category')

    def get_region(self, obj):
        return obj.get_region_display()


class PointDetailedSerializer(ModelSerializer):
    category = StringRelatedField(read_only=True, many=True)
    contacts = ContactSerializer(read_only=True, many=True)

    class Meta:
        model = PointModel
        fields = ('id', 'name', 'description', 'category', 'contacts')

    def get_region(self, obj):
        return obj.get_region_display()

    def to_representation(self, instance):
        data = super(PointDetailedSerializer, self).to_representation(instance)

        data['address'] = {
                              'region': self.get_region(instance),
                              'city': instance.city,
                              'zipCode': instance.zip_code,
                              'line1': instance.line1,
                              'geoPosition': {
                                  'lat': instance.geo_lat,
                                  'lng': instance.geo_lng
                              }
                          },
        return data


class ArticleSerializer(ModelSerializer):
    category = StringRelatedField(read_only=True, many=True)

    class Meta:
        model = ArticleModel
        fields = ('name', 'description', 'category')


class NeedsSerializer(ModelSerializer):
    article = ArticleSerializer()
    status = SerializerMethodField()

    class Meta:
        model = NeedModel
        fields = ('id', 'point', 'status', 'article')

    def get_status(self, obj):
        return obj.get_status_display()

    def to_representation(self, instance):
        data = super(NeedsSerializer, self).to_representation(instance)

        data['name'] = instance.article.name
        data['description'] = instance.article.description

        data['quantity'] = {
           'needed': instance.quantity_needed,
           'done': instance.quantity_done,
        },
        data['units'] = instance.units

        data['category'] = data.get('article').get('category')
        data.pop('article')

        return data








# from .models import HospitalNeedModel, ArticleModel, CategoryModel, HospitalModel
#
#
# class HospitalSerializer(ModelSerializer):
#     region = SerializerMethodField()
#
#     class Meta:
#         model = HospitalModel
#         fields = ('name', 'region', 'contact_person', 'email', 'tel')
#
#     def get_region(self, obj):
#         return obj.get_region_display()
#
#
# class CategorySerializer(ModelSerializer):
#     class Meta:
#         model = CategoryModel
#         fields = ('name',)
#
#
# class ArticleSerializer(ModelSerializer):
#     category = CategorySerializer()
#
#     class Meta:
#         model = ArticleModel
#         fields = ('name', 'category')
#
#
# class HospitalNeedSerializer(ModelSerializer):
#     hospital = HospitalSerializer()
#     article = ArticleSerializer()
#     units = SerializerMethodField()
#     status = SerializerMethodField()
#
#     class Meta:
#         model = HospitalNeedModel
#         depth = 2
#         fields = ('hospital', 'article', 'count', 'units', 'status', 'last_edited_on')
#
#     def get_units(self, obj):
#         return obj.get_units_display()
#
#     def get_status(self, obj):
#         return obj.get_status_display()