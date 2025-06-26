from django.db import models

class user_info_extend(models.Model):
    app_id = models.CharField(max_length=64)
    user_id = models.CharField(max_length=36)
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    id_document = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return f"{self.name} {self.last_name} ({self.user_id})"
