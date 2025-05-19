from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    #El related_name es el nombre que se usará para acceder a los posts desde el usuario, desde el HTML
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name="Usuario")
    image = models.ImageField(upload_to="posts_images/", verbose_name="Imagen")
    caption = models.TextField(blank=True, verbose_name="Descripción")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True,verbose_name="Nº de likes")

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return f"Post de {self.user.username} - {self.created_at}"    
    
class Comment(models.Model):
    post= models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text= models.TextField("Contenido del comentario", max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    class Meta:
        verbose_name = "Comentario"
        verbose_name_plural = "Comentarios"

    def __str__(self):
        return f"Comentario de {self.user.username} en {self.post.id}" # type: ignore