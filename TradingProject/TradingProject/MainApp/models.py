from django.db import models

class Candle(models.Model):
    id = models.IntegerField(primary_key=True)
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    date = models.DateTimeField()
    timeframe = models.CharField(max_length=255)

    def __str__(self):
        return f"Candle (ID: {self.id}, Open: {self.open}, High: {self.high}, Low: {self.low}, Close: {self.close}, Date: {self.date})"
    
    class Meta:
        app_label = 'MainApp'
