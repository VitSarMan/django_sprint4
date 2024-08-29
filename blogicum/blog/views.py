import datetime
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from blogicum import settings
from django.http import Http404
from .models import Category, Post, Comments

from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from django.contrib.auth import get_user_model
from django.urls import reverse
from .forms import PostForm, CommentsForm
from django.db.models import Count

class OnlyAuthorMixin(UserPassesTestMixin):
    def test_func(self):
        object = self.get_object()
        if hasattr(object, 'username'):
            return object.username == self.request.user.username
        elif hasattr(object, 'author'):
            return object.author.username == self.request.user.username


class UserMixin:
    model = get_user_model()
    slug_url_kwarg = 'username'
    slug_field = 'username'


class UserDetailView(UserMixin, DetailView):
    template_name = 'blog/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.object
        if self.request.user == self.object:
            user_posts = Post.objects.filter(author=self.object.id)
        else:
            user_posts = Post.published.filter(author=self.object.id)

        user_posts = user_posts.annotate(comment_count=Count('comments')).order_by('-pub_date')

        paginator = Paginator(user_posts, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context['user'] = self.request.user
        context['page_obj'] = page_obj
    
        return context
    

class UserUpdateView(OnlyAuthorMixin, UserMixin, UpdateView):
    template_name = 'blog/user.html'
    fields = ['first_name', 'last_name', 'username', 'email']
    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username': self.object.username})


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username': self.request.user.username})

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostsListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    queryset = Post.published.all().prefetch_related('category', 'location').select_related('author').filter(category__is_published=True)
    ordering = '-pub_date'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(comment_count=Count('comments'))
        return queryset



# class PostDetailView(DetailView):
#     model = Post
#     form_class = PostForm
#     template_name = 'blog/detail.html'
#     def get_object(self):
#         post_id = self.kwargs.get("post_id")
#         return get_object_or_404(Post, id=post_id)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         post = self.get_object()
#         context['form'] = CommentsForm()
#         context['comments'] = post.comments_set.all()
#         return context

class PostDetailView(DetailView):
    model = Post
    form_class = PostForm
    template_name = 'blog/detail.html'

    def get_object(self):
        post_id = self.kwargs.get("post_id")
        post = get_object_or_404(Post, id=post_id)

        # Проверка, опубликован ли пост
        if not post.is_published:
            raise Http404("Пост не опубликован")

        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['form'] = CommentsForm()
        context['comments'] = post.comments_set.all()
        return context


# class CategoryListView(ListView):
#     model = Post
#     template_name = 'blog/category.html'
#     paginate_by = 10

#     def get_queryset(self):
#         category_slug = self.kwargs.get('category_slug')
        
#         # Получаем категорию и проверяем, опубликована ли она
#         category = get_object_or_404(Category, slug=category_slug)
#         if not category.is_published:
#             return Post.objects.none()  # Возвращаем пустой QuerySet, если категория не опубликована
        
#         queryset = Post.published.filter(category=category)
#         queryset = queryset.prefetch_related('category', 'location').select_related('author')
#         queryset = queryset.annotate(comment_count=Count('comments')).order_by('-pub_date')
#         return queryset

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         category_slug = self.kwargs.get('category_slug')
#         # Получаем категорию и добавляем её в контекст
#         category = get_object_or_404(Category, slug=category_slug)
#         context['category'] = category
        
#         return context


class CategoryListView(ListView):
    model = Post
    template_name = 'blog/category.html'
    paginate_by = 10

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        
        # Получаем категорию и проверяем, опубликована ли она
        category = get_object_or_404(Category, slug=category_slug)
        if not category.is_published:
            raise Http404("Категория не опубликована")  # Вызываем 404, если категория не опубликована
        
        queryset = Post.published.filter(category=category)
        queryset = queryset.prefetch_related('category', 'location').select_related('author')
        queryset = queryset.annotate(comment_count=Count('comments')).order_by('-pub_date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get('category_slug')
        
        # Получаем категорию и добавляем её в контекст
        category = get_object_or_404(Category, slug=category_slug)
        context['category'] = category
        
        return context

class PostDeleteView(OnlyAuthorMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'
    def get_object(self, queryset=None):
        post_id = self.kwargs.get('post_id')
        return get_object_or_404(Post, id=post_id)

    def get_success_url(self):
        return reverse('blog:index') 
    

class PostUpdateView(OnlyAuthorMixin, UpdateView):
    model = Post
    template_name = 'blog/detail.html'
    form_class = PostForm

    def get_object(self):
        post_id = self.kwargs.get("post_id")
        return get_object_or_404(Post, id=post_id)


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comments
    template_name = 'blog/comment.html'
    form_class = CommentsForm

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        form.instance.post = post
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'post_id': self.object.post.id})
    

class CommentUpdateView(OnlyAuthorMixin, UpdateView):
    model = Comments
    template_name = 'blog/comment.html'
    fields = ['text']

    def get_object(self, queryset=None):
        comment_id = self.kwargs.get('comment_id')
        return get_object_or_404(Comments, id=comment_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment'] = self.get_object()
        return context
    
    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'post_id': self.object.post.id})
    

class CommentDeleteView(OnlyAuthorMixin, DeleteView):
    model = Comments
    template_name = 'blog/comment.html'
    
    def get_object(self, queryset=None):
        comment_id = self.kwargs.get('comment_id')
        return get_object_or_404(Comments, id=comment_id)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'post_id': self.object.post.id}) 


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

