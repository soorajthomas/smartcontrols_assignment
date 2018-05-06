from rest_framework import serializers


class HotelSerializer(serializers.Serializer):
    name = serializers.CharField()
    price = serializers.FloatField()
    city = serializers.CharField()
    image_url = serializers.URLField()
