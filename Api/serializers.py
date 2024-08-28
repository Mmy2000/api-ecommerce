from rest_framework import serializers
from  store.models import Category, Product , Review , Cart , Cartitems

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ["category_id", "title", "slug"]


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Product
        fields = [ "id", "name", "description", "category", "slug", "inventory", "old_price", "price","discount","image"]


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "date_created", "name", "description"]
    
    def create(self, validated_data):
        product_id = self.context["product_id"]
        return Review.objects.create(product_id = product_id,  **validated_data)
    
class CartSerializer(serializers.ModelSerializer):
    cart_id = serializers.UUIDField(read_only=True)
    class Meta:
        model = Cart
        fields = ["cart_id"]