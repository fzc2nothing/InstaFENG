from annoying.decorators import ajax_request
from django.views.generic import TemplateView, ListView,DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse,reverse_lazy
from  Insta.models import Post,Like,InstaUser

from django.contrib.auth.mixins import LoginRequiredMixin

from Insta.forms import CustomUserCreationForm

class HelloWorld(TemplateView):
    template_name = 'test.html'

class PostsView(ListView):
    model = Post
    template_name = 'index.html'

class PostDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"

class UserDetailView(DetailView):
    model = InstaUser
    template_name = "user_detail.html"

    # def get_context_data(self, **kwargs):
    #     data = super().get_context_data(**kwargs)
    #     liked = Like.objects.filter(post=self.kwargs.get('pk'), user=self.request.user).first()
    #     if liked:
    #         data['liked'] = 1
    #     else:
    #         data['liked'] = 0
    #     return data
class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    template_name = "post_create.html"
    fields = '__all__'
    login_url = 'login'

class PostUpdateView(UpdateView):
    model = Post
    fields = ['title']
    template_name = 'post_update.html'

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts')

class SignUp(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

@ajax_request
def addLike(request):
    post_pk = request.POST.get('post_pk')
    post = Post.objects.get(pk=post_pk)
    try:
        like = Like(post=post, user=request.user)
        like.save()
        result = 1
    except Exception as e:
        like = Like.objects.get(post=post, user=request.user)
        like.delete()
        result = 0

    return {
        'result': result,
        'post_pk': post_pk
    }

# Create your views here.


