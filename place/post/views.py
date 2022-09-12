from urllib import request

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView

from accprofile.models import Profile
from .forms import PostForm
from .models import PostNews
from accprofile.models import SubscripModel


class NewPost(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'post/create_post.html'
    login_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# class PostView(DetailView):
#     model = PostNews
#     template_name = 'post/post_view.html'
#     context_object_name = 'post'

def feed(request):
    follow_list = SubscripModel.objects.filter(follower=request.user)
    feed = PostNews.objects.filter(author__in=follow_list.values_list('author')).order_by('-created_at')
    return render(request, 'post/feed.html', context={'feed': feed})

@login_required
def postview(request, slug):
    authorpost = PostNews.objects.get(slug=slug)
    author = authorpost.author
    profile = User.objects.get(username=author)

    following_list = SubscripModel.objects.filter(author=profile, follower=request.user)
    # follow_list = SubscripModel.objects.filter(follower__in=following_list.values('follower'))

    return render(request, 'post/post_view.html', context={'follow_list': following_list, 'post': authorpost})


class Search(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('query')

        menu_items = PostNews.objects.filter(title__icontains=query)
        peopls = Profile.objects.filter(user__username__icontains=query)
        context = {
            'results': menu_items,
            'peopls': peopls
        }
        return render(request, 'post/search.html', context)


def pay(request, slug):
    owner = Profile.objects.get(slug=slug)

    payscore = request.user.profile.monet
    payscore -= owner.subprice

    request.user.profile.monet = payscore
    request.user.profile.save()

    profile = Profile.objects.get(user=owner.user)

    profile.monet += profile.subprice

    profile.save()
    ko4 = User.objects.get(username=profile.user)

    author = ko4
    follower = request.user
    list_follow = SubscripModel.objects.filter(author=author, follower=follower)
    if not list_follow:
        list_follow = SubscripModel(author=author, follower=follower)
        list_follow.save()

    return redirect('home')
