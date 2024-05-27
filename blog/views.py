from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView
from pytils.translit import slugify

from blog.models import Blog


class BlogCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Класс создания статьи блога."""
    model = Blog
    fields = ('blog_title', 'blog_description', 'blog_image', 'is_published',)
    permission_required = ('blog.add_blog',)
    success_url = reverse_lazy('blog:blog_list')

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.blog_title)
            new_blog.save()
        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Класс редактирования статьи блога."""
    model = Blog
    fields = ('blog_title', 'blog_description', 'blog_image', 'is_published',)
    permission_required = ('blog.change_blog',)

    def form_valid(self, form):
        if form.is_valid():
            blog = form.save()
            blog.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:view', args=[self.kwargs.get('pk')])


class BlogListView(LoginRequiredMixin, ListView):
    """Класс просмотра списка статей блога."""
    model = Blog
    template_name = 'blog_list.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogDetailView(LoginRequiredMixin, DetailView):
    """Класс просмотра статьи блога."""
    model = Blog

    def get(self, request, pk, **kwargs):
        blog = self.get_object()
        context = {
            'object_list': Blog.objects.filter(pk=pk),
        }
        return render(request, 'blog/blog_detail.html', context)

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Класс удаления статьи блога."""
    model = Blog
    permission_required = ('blog.delete_blog',)
    success_url = reverse_lazy('blog:blog_list')
