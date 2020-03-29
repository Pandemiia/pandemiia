from rest_framework.serializers import ModelSerializer, StringRelatedField, SerializerMethodField
from .models import HospitalNeedModel, ArticleModel, CategoryModel, HospitalModel


class HospitalSerializer(ModelSerializer):
    region = SerializerMethodField()

    class Meta:
        model = HospitalModel
        fields = ('name', 'region', 'contact_person', 'email', 'tel')

    def get_region(self, obj):
        return obj.get_region_display()


class CategorySerializer(ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = ('name',)


class ArticleSerializer(ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = ArticleModel
        fields = ('name', 'category')


class HospitalNeedSerializer(ModelSerializer):
    hospital = HospitalSerializer()
    article = ArticleSerializer()
    units = SerializerMethodField()
    status = SerializerMethodField()

    class Meta:
        model = HospitalNeedModel
        depth = 2
        fields = ('hospital', 'article', 'count', 'units', 'status', 'last_edited_on')

    def get_units(self, obj):
        return obj.get_units_display()

    def get_status(self, obj):
        return obj.get_status_display()