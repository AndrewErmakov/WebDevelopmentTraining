from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView

from posts_app.models import Post


class PostsListView(ListView):
    model = Post
    template_name = 'home.html'


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'create_post.html'
    fields = ('title', 'content',)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
