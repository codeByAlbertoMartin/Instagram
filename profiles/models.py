from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField("Imagen de perfil", upload_to="profile_pictures/", blank=True, null=True)
    bio = models.TextField("Biografía", blank=True, null=True)
    birth_date = models.DateField("Fecha de nacimiento", blank=True, null=True)
    
    # followers es una relación de muchos a muchos con el mismo modelo UserProfile,
    # lo que significa que un usuario puede seguir a muchos otros usuarios y ser seguido por muchos otros usuarios.
    #symmetrical=False significa que la relación no es simétrica, es decir, si A sigue a B, no significa que B siga a A.
    #through='Follow' indica que la relación se gestiona a través de un modelo intermedio llamado Follow (se crea sola)
    
    followers = models.ManyToManyField("self", symmetrical=False, related_name='following', through='Follow')

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfiles"
    
    def __str__(self):
        return self.user.username
    
    def follow(self,profile):
        Follow.objects.get_or_create(follower=self, following=profile) 


class Follow(models.Model):
    follower = models.ForeignKey(UserProfile, verbose_name="¿Quién sigue?", on_delete=models.CASCADE, related_name='follower_set')
    following= models.ForeignKey(UserProfile, verbose_name="¿A quién sigue?", on_delete=models.CASCADE, related_name='following_set')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="¿Desde cuándo lo sigue?")

    class Meta:
        verbose_name = "Seguidor"
        verbose_name_plural = "Seguidores"
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower} sigue a {self.following}"
    
    