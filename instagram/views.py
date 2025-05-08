from django.shortcuts import HttpResponseRedirect


# Create your views here.
#cual es la difierencia entre reverselazy y reverse
# reverse_lazy se utiliza para redirigir a una vista que no existe en el momento de la carga de la vista
# reverse se utiliza para redirigir a una vista que existe en el momento de la carga de la vista
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView,FormView
from  django.contrib.auth.models import User
from .forms import RegistrationForm, LoginForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout

class HomeView(TemplateView):
    template_name = "general/home.html"


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


class LegalView(TemplateView):
    template_name = "general/legal.html"



class ContactView(TemplateView):
    template_name = "general/contact.html"


def logout_view(request):
    logout(request)
    messages.add_message(request, messages.INFO, 'Has cerrado sesión correctamente')
    return HttpResponseRedirect(reverse('home'))