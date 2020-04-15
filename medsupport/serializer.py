from rest_framework.serializers import ModelSerializer, StringRelatedField, \
    PrimaryKeyRelatedField, SerializerMethodField
from .models import NeedModel, PointModel, CategoryPointModel, ContactModel, ArticleModel, CategoryArticleModel


class CategoryPointSerializer(ModelSerializer):
    class Meta:
        model = CategoryPointModel
        fields = ('name',)


class CategoryArticleSerializer(ModelSerializer):
    class Meta:
        model = CategoryArticleModel
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


class ArticleSerializer(ModelSerializer):
    category = StringRelatedField(read_only=True, many=True)

    class Meta:
        model = ArticleModel
        fields = ('name', 'description', 'category')


class NeedsSerializer(ModelSerializer):
    article = ArticleSerializer()
    status = SerializerMethodField()
    units = SerializerMethodField()

    class Meta:
        model = NeedModel
        fields = ('id', 'point', 'status', 'article', 'units')

    def get_status(self, obj):
        return obj.get_status_display()

    def get_units(self, obj):
        return obj.get_units_display()

    def to_representation(self, instance):
        data = super(NeedsSerializer, self).to_representation(instance)

        data['name'] = instance.article.name
        data['description'] = instance.article.description

        q = {'quantity': {
           'needed': instance.quantity_needed,
           'done': instance.quantity_done,
        }}
        data.update(q)

        data['category'] = data.get('article').get('category')
        data.pop('article')

        return data
