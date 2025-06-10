from rest_framework import serializers
from .models import FitnessClass, Booking
from .utils import convert_ist_to_tz


class FitnessClassSerializer(serializers.ModelSerializer):
    """
    Serializer for FitnessClass model.
    Formats datetime based on requested timezone (defaults to Asia/Kolkata).
    """
    datetime = serializers.SerializerMethodField()

    class Meta:
        model = FitnessClass
        fields = ['id', 'name', 'instructor', 'datetime', 'available_slots']

    def get_datetime(self, obj):
        """
        Convert datetime from IST to requested timezone.
        """
        tz = self.context.get('timezone', 'Asia/Kolkata')
        return convert_ist_to_tz(obj.datetime, tz)


class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for Booking model. Returns all booking details.
    """
    class Meta:
        model = Booking
        fields = '__all__'
