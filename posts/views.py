from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView
from posts.models import Post
from .forms import PostCreateForm
from django.urls import reverse, reverse_lazy
from django.contrib import messages 
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.http import JsonResponse


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

class PostDetailView(DetailView):
    model=Post
    template_name="posts/post_detail.html"
    context_object_name = "post"

@login_required
def like_post(request, pk):
    post = Post.objects.get(pk=pk)
    if request.user in post.likes.all():
        messages.add_message(request, messages.INFO, "Ya no me gusta la publicación")
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        messages.add_message(request, messages.INFO, "Te gusta la publicación")

    return HttpResponseRedirect(reverse("post_detail", args=[pk]))
    

@login_required
def like_post_ajax(request, pk):
    post = Post.objects.get(pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        return JsonResponse(
            {
                'message': "Ya no me gusta esta publicación",
                'liked':False,
                'nLikes': post.likes.all().count()
            }
        )
    else:
        post.likes.add(request.user)
        return JsonResponse(
            {
                'message': "Te gusta esta publicación",
                'liked':True,
                'nLikes': post.likes.all().count()
            }
        )
