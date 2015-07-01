from django.db import models

class Currency(models.Model):
    """
    Currencies list.
    """
    name = models.CharField(max_length=10)
    description = models.TextField()

    def __str__(self):
        return '{0} {1}'.format(self.name, self.description)

    class Meta:
        verbose_name_plural = "Currencies"

class Rate(models.Model):
    """
    Rates list.
    """
    currency = models.ForeignKey(Currency, related_name="rates")
    value = models.DecimalField(max_digits=19, decimal_places=10)
    obsolete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{0} {1} {2} {3}'.format(self.currency.name, self.value, self.created, self.obsolete)
