from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Count
from django.views.generic import UpdateView, ListView
from django.utils import timezone
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User

from .models import Board, Topic, Post
from .forms import NewTopicForm, PostForm


class BoardListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'boards/home.html'


# def board_topic_view(request, pk):
#     board = get_object_or_404(Board, pk=pk)
#     queryset = board.topics.order_by('-last_updated').annotate(replies=Count('posts'))
#
#     page = request.GET.get('page', 1)
#     paginator = Paginator(queryset, 20)
#
#     try:
#         topics = paginator.page(page)
#     except PageNotAnInteger:
#         topics = paginator.page(1)
#     except EmptyPage:
#         topics = paginator.page(paginator.num_pages)
#
#     return render(request, 'boards/topics.html', {'board': board, 'topics': topics})


class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'boards/topics.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
        queryset = self.board.topics.order_by('-last_updated').annotate(replies=Count('posts'))
        return queryset


@login_required
def new_topic_view(request, pk):
    board = get_object_or_404(Board, pk=pk)
    # user = get_current_user(request)
    # user = User.objects.all().first()

    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()

            post = Post.objects.create(
                    message=form.cleaned_data['message'],
                    topic=topic,
                    created_by=request.user
            )
            return redirect('boards:topic_posts', pk=pk, topic_pk=topic.pk)
    else:
        form = NewTopicForm()
    return render(request, 'boards/new_topic.html', {'board': board, 'form': form})


# def topic_posts_view(request, pk, topic_pk):
#     topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
#     topic.views += 1
#     topic.save()
#     return render(request, 'boards/topic_posts.html', {'topic': topic})


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'boards/topic_posts.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        session_key = 'topic_{}'.format(self.topic.pk)
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True

        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset


@login_required
def reply_view(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        f = PostForm(request.POST)
        if f.is_valid():
            post = f.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()

            topic.last_updated = timezone.now()
            topic.save()

            topic_url = reverse('boards:topic_posts', kwargs={'pk': pk, 'topic_pk': topic_pk})
            topic_post_url = '{url}?page={page}#{id}'.format(
                url=topic_url,
                page=topic.get_page_count(),
                id=post.pk
            )
            return redirect(topic_post_url)
    else:
        f = PostForm()
    return render(request, 'boards/reply.html', {'form': f, 'topic': topic})


@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message', )
    template_name = 'boards/edit.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        form.updated_by = self.request.user
        form.updated_at = timezone.now()
        post.save()
        return redirect('boards:topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)


@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email')
    template_name = 'boards/my_account.html'
    success_url = reverse_lazy('boards:account')

    def get_object(self):
        return self.request.user
