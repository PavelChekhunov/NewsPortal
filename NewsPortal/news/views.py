from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Author, Subscribe, Category
from .filters import PostFilter
from .forms import NewsForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from datetime import date
from .tools import page_videos
import logging
# from .tasks import newsletter
# from NewsPortal.celery import app as celery_app


# def _is_celery_working():
#     try:
#         celery_app.broker_connection(connect_timeout=1).ensure_connection(max_retries=1)
#         return True
#     except Exception:
#         return False


class PostsList(ListView):
    model = Post
    ordering = '-datetime_created'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 15

    def __init__(self):
        super().__init__()
        self.filterset = None

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['postimg'] = [8]
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if context['post'].category.first():
            context['fcat'] = context['post'].category.first().name
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        if context['is_author']:
            cur_author = Author.objects.filter(user=self.request.user)
            context['is_current_author'] = cur_author.exists() and cur_author[0] == self.object.author
        if self.object.pk in page_videos():
            context['page_vid'] = page_videos()[self.object.pk]

        return context


class PostDetailImage(PostDetail):
    template_name = 'post_img.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['img_src'] = 'img1.png'
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context


class PostSearch(PostsList):
    template_name = 'search.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['postimg'] = [8]
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context


class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = NewsForm
    model = Post
    template_name = 'post_create.html'
    pk_url_kwarg = 'id'

    permission_required = ('news.add_post', 'news.view_post')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        context['post_counter'] = 0
        if context['is_author']:
            cur_author = Author.objects.filter(user=self.request.user)
            if cur_author.exists():
                context['post_counter'] = (Post.objects.filter(author=cur_author[0])
                                           .filter(datetime_created__startswith=date.today()).count())
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = Author.objects.get(user=self.request.user)
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        retval = super().post(request, *args, **kwargs)
        # send_email_notification(request, self.object)
        # if _is_celery_working():
        #     newsletter.apply_async([self.object.id], countdown=3, expires=15)
        return retval


class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = NewsForm
    model = Post
    template_name = 'post_edit.html'
    pk_url_kwarg = 'id'

    permission_required = ('news.change_post', 'news.view_post')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        if context['is_author']:
            cur_author = Author.objects.filter(user=self.request.user)
            context['is_current_author'] = cur_author.exists() and cur_author[0] == self.object.author
        return context


class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')
    pk_url_kwarg = 'id'

    permission_required = ('news.delete_post', 'news.view_post')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        if context['is_author']:
            cur_author = Author.objects.filter(user=self.request.user)
            context['is_current_author'] = cur_author.exists() and cur_author[0] == self.object.author
        return context


class CreateArticle(PostCreate):
    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'ART'
        post.author = Author.objects.get(user=self.request.user)
        return super().form_valid(form)


class SubscribeCategories(LoginRequiredMixin, ListView):
    model = Category
    ordering = "name"
    template_name = 'subscribe.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        if not self.request.user.is_anonymous:
            context['cat_subscribed'] = Subscribe.objects.filter(user=self.request.user).values_list('category',
                                                                                                     flat=True)
        return context


@login_required
def subscription(request):
    if not request.user.is_anonymous:
        Subscribe.objects.filter(user=request.user).delete()
        for item in request.POST.getlist('sc_cat'):
            cat = Category.objects.get(pk=item)
            cat.subscribers.add(request.user)

    return redirect('post_list')


def testlog(request):
    loggers = ('django', 'django.request', 'django.server', 'django.template', 'django.db.backends',
               'django.security')
    # loggers = ('django.request', )
    for logger in [logging.getLogger(name) for name in loggers]:
        logger.info(f"Logger: {logger.name}")
        logger.debug('testlog DEBUG message')
        logger.info('testlog INFO message')
        logger.warning('testlog WARNING message')
        logger.error('testlog ERROR message')
        logger.critical('testlog CRITICAL message')

    return redirect('post_list')
