from django.db import models
class Bus(models.Model):
    bus_id = models.IntegerField()
    route = models.IntegerField()
    passengers = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensures uniqueness
        unique_together = ('bus_id', 'timestamp')  

    def __str__(self):
        return f"Bus {self.bus_id} on Route {self.route} at {self.timestamp}"
