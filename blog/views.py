# from django.shortcuts import render, redirect
# from django.shortcuts import get_object_or_404
# from django.contrib.auth.models import User
from django.views import generic
from django.urls import reverse_lazy

from .models import Post
from .forms import PostForm


# Class-Based Views:

class PostsListView(generic.ListView):
    model = Post
    template_name = 'blog/posts_list.html'
    context_object_name = 'posts_list'

    def get_queryset(self):
        return Post.objects.filter(status='pub').order_by('-date_modified')


class PostDetailsView(generic.DetailView):
    model = Post
    template_name = 'blog/post_details.html'
    context_object_name = 'post'


class PostCreateView(generic.CreateView):
    form_class = PostForm
    template_name = 'blog/create_post.html'
    context_object_name = 'form'


class PostUpdateView(generic.UpdateView):
    model = Post
    template_name = 'blog/create_post.html'
    form_class = PostForm
    context_object_name = 'form'


class PostDeleteView(generic.DeleteView):
    model = Post
    template_name = 'blog/delete_post.html'
    success_url = reverse_lazy('posts_list')
    context_object_name = 'post'


# Functional Views:

# def posts_list_view(request):
#     posts_list = Post.objects.filter(status='pub').order_by('-date_modified')
#     return render(request, 'blog/posts_list.html', {'posts_list': posts_list})


# def post_details_view(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     return render(request, 'blog/post_details.html', {'post': post})


# def post_create_view(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('posts_list')
#             # form = PostForm()
#
#     else:  # Get request
#         form = PostForm()
#
#     return render(request, 'blog/create_post.html', context={'form': form})


# def post_update_view(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     form = PostForm(request.POST or None, instance=post)
#
#     if form.is_valid():
#         form.save()
#         return redirect('posts_list')
#
#     return render(request, 'blog/create_post.html', context={'form': form})


# def post_delete_view(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#
#     if request.method == 'POST':
#         post.delete()
#         return redirect('posts_list')
#
#     return render(request, 'blog/delete_post.html', context={'post': post})
