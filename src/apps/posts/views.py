from django.shortcuts import render, redirect
from django_refresher.src.apps.posts.models import Post, Like
from django_refresher.src.apps.profiles.models import Profile
from django.urls import reverse_lazy
from django_refresher.src.apps.posts.forms import PostModelForm, CommentModelForm
from django.views.generic import UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
@login_required
def post_comment_create_and_list_view(request):
    query_set = Post.objects.all()
    profile = Profile.objects.get(user=request.user)

    # Post form, comment form
    p_form = PostModelForm()
    c_form = CommentModelForm()
    post_added = False
    
    profile = Profile.objects.get(user=request.user)

    if 'submit_p_form' in request.POST:
        p_form = PostModelForm(request.POST, request.FILES)
        if p_form.is_valid():
            instance = p_form.save(commit=False) # not commiting(saving) here because we need to splice in the profile as the author
            instance.author = profile
            instance.save()
            p_form = PostModelForm()
            post_added = True

    if 'submit_c_form' in request.POST:
        c_form = CommentModelForm(request.POST)
        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.user = profile
            instance.post = Post.objects.get(id=request.POST.get('post_id'))
            instance.save()
            c_form = CommentModelForm()

    context = {
        'query_set' : query_set,
        'profile': profile,
        'p_form': p_form,
        'c_form': c_form,
        'post_added' : post_added
    }

    return render(request, 'posts/main.html', context)

@login_required
def like_toggle_post(request):
    user = request.user

    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=user)

        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile)
        
        like, created = Like.objects.get_or_create(user=profile, post_id=post_id)

        if not created:
            if like.value == 'Like':
                like.value='Unlike'
            else:
                like.value='Like'
        else:
            like.value='Like'
        
        post_obj.save()
        like.save()
    
        data = {
            'value': like.value,
            'likes': post_obj.liked.all().count()
        }
        return JsonResponse(data, safe=False)
    
    return redirect('posts:main-post-view')

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'posts/confirm_del.html'
    success_url = reverse_lazy('posts:main-post-view')

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        obj = Post.objects.get(pk=pk)
        if not obj.author.user == self.request.user:
            messages.warning(self.request, 'You can only delete your own posts!')
        return obj

class PostUpdateView(LoginRequiredMixin, UpdateView):
    form_class = PostModelForm # specified in forms.py
    template_name = 'posts/update.html'
    success_url = reverse_lazy('posts:main-post-view')
    model = Post

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        if form.instance.author == profile:
            return super().form_valid(form)
        else:
            form.add_error(None, "You can only edit your own posts!")
            return super().form_invalid(form)