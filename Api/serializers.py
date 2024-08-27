from rest_framework import serializers
from  store.models import Category, Product

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ["category_id", "title", "slug"]

        
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Product
        fields = [ "id", "name", "description", "category", "slug", "inventory", "old_price", "price","discount"]

