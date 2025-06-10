from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now
from pytz import timezone
from pytz.exceptions import UnknownTimeZoneError

from .models import FitnessClass, Booking
from .serializers import FitnessClassSerializer, BookingSerializer
from .utils import get_logger

# Logger setup
logger = get_logger(__name__)

# Default timezone
DEFAULT_TZ = 'Asia/Kolkata'


@api_view(['GET'])
def index(request):
    """
    Root endpoint providing available API routes.
    """
    logger.info("Accessed index endpoint")
    return Response({
        "message": "Welcome to the Fitness Booking API",
        "endpoints": {
            "GET /classes": "List all upcoming fitness classes",
            "POST /book": "Book a class",
            "GET /bookings?email=someone@example.com": "Get bookings by email"
        }
    })


@api_view(['GET'])
def list_classes(request):
    """
    Returns a list of all future fitness classes.
    Optional query param:
    - tz: Target timezone (defaults to Asia/Kolkata)
    """
    tz_param = request.query_params.get('tz', DEFAULT_TZ)
    try:
        target_tz = timezone(tz_param)
    except UnknownTimeZoneError:
        logger.warning(f"Invalid timezone requested: {tz_param}")
        return Response({'error': 'Invalid timezone'}, status=status.HTTP_400_BAD_REQUEST)

    upcoming_classes = FitnessClass.objects.filter(datetime__gte=now())

    # Convert each datetime to the target timezone
    for cls in upcoming_classes:
        cls.datetime = cls.datetime.astimezone(target_tz)

    serializer = FitnessClassSerializer(upcoming_classes, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def book_class(request):
    """
    Accepts a booking request and books a class if slots are available.
    Required fields: class_id, client_name, client_email
    Handles errors: missing fields, overbooking, invalid class ID
    """
    data = request.data
    required_fields = ['class_id', 'client_name', 'client_email']

    if not all(field in data for field in required_fields):
        logger.error("Booking failed due to missing required fields.")
        return Response(
            {'error': 'Missing required fields: class_id, client_name, client_email'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        fitness_class = FitnessClass.objects.get(id=data['class_id'])
    except FitnessClass.DoesNotExist:
        logger.error(f"Booking failed: Class ID {data['class_id']} not found.")
        return Response({'error': 'Class not found.'}, status=status.HTTP_404_NOT_FOUND)

    if fitness_class.available_slots <= 0:
        logger.info(f"Booking failed: Class {fitness_class.name} is fully booked.")
        return Response({'error': 'Class is fully booked.'}, status=status.HTTP_400_BAD_REQUEST)

    booking = create_booking(data, fitness_class)
    logger.info(f"Booking created successfully for {data['client_email']} in class '{fitness_class.name}'.")

    return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)


def create_booking(data, fitness_class):
    """
    Helper function to create a booking and update class slots.
    """
    booking = Booking.objects.create(
        fitness_class=fitness_class,
        client_name=data['client_name'],
        client_email=data['client_email']
    )
    fitness_class.available_slots -= 1
    fitness_class.save()
    return booking


@api_view(['GET'])
def get_bookings_by_email(request):
    """
    Returns all bookings for a client based on email query param.
    Optional query param:
    - tz: Target timezone for class datetime
    """
    email = request.query_params.get('email')
    if not email:
        logger.error("Bookings fetch failed: email not provided.")
        return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

    tz_param = request.query_params.get('tz', DEFAULT_TZ)
    try:
        target_tz = timezone(tz_param)
    except UnknownTimeZoneError:
        logger.warning(f"Invalid timezone requested in bookings: {tz_param}")
        return Response({'error': 'Invalid timezone'}, status=status.HTTP_400_BAD_REQUEST)

    bookings = Booking.objects.filter(client_email=email)

    for booking in bookings:
        booking.fitness_class.datetime = booking.fitness_class.datetime.astimezone(target_tz)

    logger.info(f"Returned bookings for {email}")
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data)
