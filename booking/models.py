from django.db import models

class FitnessClass(models.Model):
    """
    Represents a scheduled fitness class with available slots.
    """
    name = models.CharField(max_length=100)
    instructor = models.CharField(max_length=100)
    datetime = models.DateTimeField()
    available_slots = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} by {self.instructor} on {self.datetime.strftime('%Y-%m-%d %H:%M')}"

class Booking(models.Model):
    """
    Represents a booking made by a client for a fitness class.
    """
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client_name} - {self.fitness_class.name} ({self.client_email})"
