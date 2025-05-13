from django.views.generic.edit import CreateView
from posts.models import Post
from .forms import PostCreateForm
from django.urls import reverse_lazy
from django.contrib import messages 
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@method_decorator(login_required, name='dispatch')# Proteger la vista para que solo los usuarios logueados puedan acceder
class PostCreateView(CreateView):
    model=Post
    template_name = "posts/post_create.html"
    form_class= PostCreateForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.add_message(self.request, messages.SUCCESS, 'Post creado correctamente')
        return super(PostCreateView, self).form_valid(form)
