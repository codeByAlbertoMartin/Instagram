from django.shortcuts import HttpResponseRedirect


# Create your views here.
#cual es la difierencia entre reverselazy y reverse
# reverse_lazy se utiliza para redirigir a una vista que no existe en el momento de la carga de la vista
# reverse se utiliza para redirigir a una vista que existe en el momento de la carga de la vista
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.edit import CreateView,FormView, UpdateView
from  django.contrib.auth.models import User
from .forms import RegistrationForm, LoginForm, ProfileFollow
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from profiles.models import UserProfile, Follow
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from posts.models import Post

class HomeView(TemplateView):
    template_name = "general/home.html"


    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        #Si el usuario está logueado
        if self.request.user.is_authenticated:
            # Obtenemos los usuarios que seguimos
            seguidos = Follow.objects.filter(following = self.request.user.profile).values_list("follower__user", flat=True) # type: ignore
            print(seguidos)
            last_posts = Post.objects.filter(user__profile__user__in=seguidos)
        else:
            last_posts = Post.objects.all().order_by('-created_at')[:5]
        context['last_posts'] = last_posts

        return context


class LoginView(FormView):
    template_name = "general/login.html"
    form_class = LoginForm  

    def form_valid(self, form):
        usuario = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=usuario, password=password)

        if user is not None:
            login(self.request, user)
            messages.add_message(self.request, messages.SUCCESS, f"Bienvenido {user.username}")
            return HttpResponseRedirect(reverse('home'))
        else:
            messages.add_message(self.request, messages.ERROR, 'Usuario o contraseña incorrectos')
            return super(LoginView, self).form_invalid(form)


class RegisterView(CreateView):
    template_name = "general/register.html"
    model = User
    success_url = reverse_lazy('login')
    form_class = RegistrationForm

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Usuario creado correctamente')
        form.save()
        return super(RegisterView, self).form_valid(form)

@method_decorator(login_required, name='dispatch')# Proteger la vista para que solo los usuarios logueados puedan acceder
class ProfileDetailView(DetailView, FormView):
    template_name = "general/profile_detail.html"
    model=UserProfile
    context_object_name = 'profile'
    form_class= ProfileFollow

    # Selecciona el perfil sobre el que se esta haciendo la accion para que el formulario ya lo sepa
    def get_initial(self):
        self.initial["profile_pk"] = self.get_object().pk
        return super().get_initial()

    def form_valid(self, form):
        profile_pk = form.cleaned_data.get("profile_pk")
        follower = UserProfile.objects.get(pk=profile_pk)

        if Follow.objects.filter(following= self.request.user.profile, follower= follower).count(): # type: ignore
            Follow.objects.filter(following= self.request.user.profile, follower= follower).delete() # type: ignore
            messages.add_message(self.request, messages.SUCCESS, f'Se ha dejado de seguir al usuario {follower.user.username}')
        else:
            Follow.objects.get_or_create(following= self.request.user.profile, follower= follower)# type: ignore
            messages.add_message(self.request, messages.SUCCESS, f'Se ha seguido al usuario {follower.user.username}')
        
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("profile_detail", args=[self.get_object().pk])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        follower = Follow.objects.filter(following= self.request.user.profile, follower= self.get_object()).exists() # type: ignore
        context["follower"] = follower

        return context


class ProfileListView(ListView):
    template_name = "general/profile_list.html"
    model=UserProfile
    context_object_name = 'profiles'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return UserProfile.objects.all().order_by('user__username').exclude(user=self.request.user)
        return UserProfile.objects.all().order_by('user__username')


@method_decorator(login_required, name='dispatch')# Proteger la vista para que solo los usuarios logueados puedan acceder
class ProfileUpdateView(UpdateView):
    template_name = "general/profile_update.html"
    model=UserProfile
    context_object_name = 'profile'
    fields = ['profile_picture', 'bio', 'birth_date']

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Usuario actualizado correctamente')
        form.save()
        return super(ProfileUpdateView, self).form_valid(form)
    
    def get_success_url(self):
        return reverse('profile_detail', kwargs={'pk': self.object.pk})# type: ignore
    
    #Sirve para comprobar si el usuario que quiere editar el perfil es el mismo que el que lo creó
    #Ademas redirecciona a la pagina de inicio si no es el mismo usuario, porque podria ser un fallo de seguridad si un
    #usuario intenta editar el perfil de otro usuario si conciera la URL
    def dispatch(self, request, *args, **kwargs):
        user_profile = self.get_object()
        if user_profile.user != self.request.user:# type: ignore
            messages.add_message(request, messages.ERROR, 'No tienes permiso para editar este perfil')
            return HttpResponseRedirect(reverse('home'))
        return super().dispatch(request, *args, **kwargs)


class LegalView(TemplateView):
    template_name = "general/legal.html"


class ContactView(TemplateView):
    template_name = "general/contact.html"


def logout_view(request):
    logout(request)
    messages.add_message(request, messages.INFO, 'Has cerrado sesión correctamente')
    return HttpResponseRedirect(reverse('home'))