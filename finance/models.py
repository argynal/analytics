from django.db import models


class Bill(models.Model):
    date = models.DateField()
    position = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    sum = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'bills'  # Укажите имя существующей таблицы в базе данных
