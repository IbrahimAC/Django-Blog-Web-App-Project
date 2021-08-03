from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse #imports always go at the top#
from.models import Post  #the '.' references which directory we are importing from. in this instance models
from.models import addressbook
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView

)


def home(request):
    context = {'posts' : Post.objects.all()} #getting the data from your DB
    return render(request, 'blog/home.html', context)

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

def bookofaddresses(request):
    info = {'addresses': addressbook.objects.all()}
    return render(request, 'blog/addressbook.html', context = info)
    #The render function accepts the request method and the template file. 
    #Note: Render still returns a http response!

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 4

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post


class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5
    
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)   

    def test_func(self):
        post = self.get_object() 
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin , UserPassesTestMixin, DeleteView): 
    model = Post
    success_url = '/' 
    def test_func(self):
      post = self.get_object()
      if self.request.user == post.author:
          return True
      return False


