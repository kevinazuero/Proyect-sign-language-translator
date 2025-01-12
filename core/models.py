from django.contrib.auth.models import AbstractUser
from django.db import models
from traductor import utils

class User(AbstractUser):
    image = models.ImageField(
        verbose_name='Archivo de imagen',
        upload_to='users',
        max_length=1024,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def get_image_url(self):
        return utils.get_image(self.image)


class Historial(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.word} - {self.date.strftime('%Y-%m-%d %H:%M')}"


class Words_state(models.Model):
    word = models.CharField(max_length=255)
    state = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.word}"
