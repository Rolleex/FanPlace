from urllib import request

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView, CreateView
from .models import *
from .forms import EditForm, CoinsForm
from post.models import PostNews


@login_required
def user(request, slug):
    profile = get_object_or_404(Profile, slug=slug)
    profilepage = profile.user
    posts = PostNews.objects.filter(author=profilepage).order_by('-created_at')
    list = SubscripModel.objects.filter(author=profilepage, follower=request.user)
    if user == request.user:
        return redirect('home')
    return render(request, 'accprofile/profile_page.html',
                  context={'profile': profile, 'posts': posts, 'list': list})


class HomeNews(ListView):
    model = Profile
    template_name = 'accprofile/home.html'
    context_object_name = 'profile'
    extra_context = {'posts': PostNews.objects.all().order_by('-created_at')}

    def get_context_data(self, **kwargs):
        context = super(HomeNews, self).get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context

    def get_queryset(self):
        return Profile.objects.all()


def edit(request):
    if request.method == 'POST':

        profile_form = EditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if profile_form.is_valid():
            profile_form.save()

            return redirect('profile', request.user.profile.slug)
    else:
        profile_form = EditForm(instance=request.user.profile)
        return render(request,
                      'accprofile/edit_profile.html',
                      {
                          'profile_form': profile_form})


class Add(LoginRequiredMixin, CreateView):
    form_class = CoinsForm
    template_name = 'accprofile/add_coins.html'
    login_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.reciver = self.request.user
        return super().form_valid(form)


class Dashboard(LoginRequiredMixin, View):
    """
    for staff. check orders for aad coins
    """

    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            orders = CoinsModel.objects.filter(is_paid=False)

            context = {
                'orders': orders,

            }

            return render(request, 'accprofile/dashboard.html', context)
        else:
            return redirect('home')


class OrderDetails(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        if request.user.is_staff:
            order = CoinsModel.objects.get(pk=pk)
            context = {
                'order': order
            }
            return render(request, 'accprofile/order-details.html', context)
        else:
            return redirect('home')

    def post(self, request, pk, *args, **kwargs):
        order = CoinsModel.objects.get(pk=pk)
        order.is_paid = True
        order.save()
        profile = Profile.objects.get(user=order.reciver)
        profile.monet += order.price
        profile.save()
        context = {
            'order': order
        }
        return redirect('dashboard')
