from django.db import models
from categorias.models import Categoria
from autores.models import Autor
import os
from django.contrib.auth.models import User
from PIL import Image
from django.conf import settings

class Livro(models.Model):
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    capa = models.ImageField(upload_to='livros_capas', verbose_name='Capa')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image(self.capa.name, 600)

    @staticmethod
    def resize_image(img_name, new_width):
        img_path = os.path.join(settings.MEDIA_ROOT, img_name)
        img = Image.open(img_path)
        width, height = img.size
        new_height = round((new_width * height) / width)

        if width <= new_width:
            img.close()
            return
        new_img = img.resize((new_width, new_height), Image.ANTIALIAS)
        new_img.save(img_path, optmize=True, quality=70)
        new_img.close()
