from django.db import models



class TrafficData(models.Model):
    location = models.CharField(max_length=255)
    density = models.IntegerField()  # Kepadatan lalu lintas (0-100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.location} - {self.density}% at {self.timestamp}"