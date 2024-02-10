from django.db import models

# Create your models here.
class Stock(models.Model):
    date = models.DateField()
    trade_code = models.CharField(max_length=200)
    high = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    low = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    open = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    close = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    volume = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    def __str__(self):
       return str(self.id)    








#    class JsonModel(models.Model):
#     date = models.DateField()
#     trade_code = models.CharField(max_length=200)
#     high = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#     low = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#     open = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#     close = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#     volume = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

#     def __str__(self):
#         return f"{self.date} - {self.trade_code}"
 