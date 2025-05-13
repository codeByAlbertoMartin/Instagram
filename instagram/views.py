from django.shortcuts import HttpResponseRedirect


# Create your views here.
#cual es la difierencia entre reverselazy y reverse
# reverse_lazy se utiliza para redirigir a una vista que no existe en el momento de la carga de la vista
# reverse se utiliza para redirigir a una vista que existe en el momento de la carga de la vista
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import CreateView,FormView, UpdateView
from  django.contrib.auth.models import User
from .forms import RegistrationForm, LoginForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from profiles.models import UserProfile
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from posts.models import Post


class HomeView(TemplateView):
    template_name = "general/home.html"


    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        
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
class ProfileDetailView(DetailView):
    template_name = "general/profile_detail.html"
    model=UserProfile
    context_object_name = 'profile'

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
        return reverse('profile_detail', kwargs={'pk': self.object.pk})


class LegalView(TemplateView):
    template_name = "general/legal.html"



class ContactView(TemplateView):
    template_name = "general/contact.html"


def logout_view(request):
    logout(request)
    messages.add_message(request, messages.INFO, 'Has cerrado sesión correctamente')
    return HttpResponseRedirect(reverse('home'))