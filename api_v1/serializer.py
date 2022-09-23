from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from webapp.models import Product, Order, OrderProduct, DEFAULT_CATEGORY, CATEGORY_CHOICES


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100, required=True)
    description = serializers.CharField(max_length=2000, required=True)
    category = serializers.ChoiceField(choices=CATEGORY_CHOICES, required=True)
    amount = serializers.IntegerField(required=True)
    price = serializers.IntegerField(required=True)

    def validate(self, attrs):
        return super().validate(attrs)

    def validate_title(self, value):
        return value

    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    def update(self, instance: Product, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ('id', 'order', 'product', 'amount', 'name')


class OrderSerializer(serializers.ModelSerializer):
    order_products = OrderProductSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'phone', 'products', 'order_products')


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("username", "id")


class ProductModelsSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    # comments = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), many=True)
    # tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, write_only=True)

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     print(instance)
    #     data["tags"] = TagSerializer(instance.tags.all(), many=True).data
    #     return data

    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")
