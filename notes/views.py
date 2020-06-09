from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from .models import Post


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'notes/post_list.html'

    def get_queryset(self):
        # todo add empty list for new user
        user = get_object_or_404(User, username=self.request.user)
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Post
    template_name = 'notes/post_detail.html'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'description']
    extra_context = {'heading': 'New Note'}

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'description']
    extra_context = {'heading': 'Edit Note'}

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def search(request):
    query = request.GET.get('q')
    if query:
        queryset = ((Q(title__icontains=query)) | (Q(description__icontains=query))) & (Q(author=request.user))
        results = Post.objects.filter(queryset).distinct()
    else:
        results = []
    return render(request, 'notes/post_list.html', {'object_list': results, 'query': query})
