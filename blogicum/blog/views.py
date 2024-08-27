import datetime

from django.shortcuts import get_object_or_404, render

from blogicum import settings

from .models import Category, Post

from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy



class UserDetailView(DetailView):
    model = get_user_model()
    slug_url_kwarg = 'username'
    slug_field = 'username'
    template_name = 'blog/profile.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.object
        return context


class PostCreateView(CreateView):
    model = Post
    fields = '__all__'
    success_url = reverse_lazy('blog:index')


def get_post_queryset():
    return Post.objects.select_related(
        'location', 'category').filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=datetime.datetime.now()
    )


def index(request):
    template = 'blog/index.html'
    post_list = get_post_queryset()[:settings.POST_LIST_GET_LENGTH]
    context = {'post_list': post_list}
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'blog/detail.html'
    post = get_object_or_404(
        get_post_queryset(),
        pk=post_id,
    )
    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    post_list = get_post_queryset().filter(category__slug=category_slug)
    context = {
        'category': category,
        'post_list': post_list
    }
    return render(request, template, context)

