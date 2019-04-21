from rest_framework import serializers

from foodtaskerapp.models import Restaurent, \
Meals, \
Customer, \
Driver, \
Order, \
OrderDetails

class RestaurentSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()

    def get_logo(self,restaurent):
        request = self.context.get('request')
        logo_url = restaurent.logo.url
        return request.build_absolute_uri(logo_url)

    class Meta:
        model = Restaurent
        fields = ("id","name","phone","address","logo")

class MealSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self,meal):
        request = self.context.get('request')
        image_url = meal.image.url
        return request.build_absolute_uri(image_url)
    class Meta:
        model = Meals
        fields = ("id","name","short_description","image","price")

#ORDER SERIALIZERS
class OrderCustomerSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source = "user.get_full_name")

    class Meta:
        model = Customer
        fields = ("id","name","avatar","phone","address")

class OrderDriverSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source = "user.get_full_name")

    class Meta:
        model = Customer
        fields = ("id","name","avatar","phone","address")

class OrderRestaurentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurent
        fields = ("id","name","phone","address")

class OrderMealSerializer(serializers.ModelSerializer):

    class Meta:
        model = Meals
        fields = ("id","name","price")

class OrderDetailsSerializer(serializers.ModelSerializer):

    meal = OrderMealSerializer
    class Meta:
        model = OrderDetails
        fields = ("id","meal","quantity","sub_total")

class OrderSerializer(serializers.ModelSerializer):

    customer = OrderCustomerSerializer()
    driver = OrderDriverSerializer()
    restaurent = OrderRestaurentSerializer()
    order_details = OrderDetailsSerializer(many = True)
    status = serializers.ReadOnlyField(source = "get_status_display")

    class Meta:
        model = Order
        fields =("id","customer","driver","restaurent","order_details","total","status","address")