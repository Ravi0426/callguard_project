from django.db import models

class Call(models.Model):
    message = models.TextField()
    label = models.BooleanField(default=False)

    def __str__(self):
        return self.message[:50]
