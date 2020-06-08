from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from .models import Post
from django.http import HttpResponse


class PostListView(ListView):
    model = Post
    template_name = 'notes/home.html'


class PostDetailView(DetailView):
    model = Post
    template_name = 'notes/post_detail.html'


class PostUpdateView(UpdateView):
    model = Post
    fields = ['title', 'description']
    extra_context = {'heading': 'Edit Note'}


class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'description']
    extra_context = {'heading': 'New Note'}

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDeleteView(DeleteView):
    model = Post
    success_url = '/'


def search(request):
    query = request.GET.get('q')
    if query:
        queryset = (Q(title__icontains=query)) | (Q(description__icontains=query))
        results = Post.objects.filter(queryset).distinct()
    else:
        results = []
    return render(request, 'notes/home.html', {'object_list': results, 'query': query})
