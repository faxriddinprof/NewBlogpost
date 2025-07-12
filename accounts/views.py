from django.shortcuts import render
from django.views.generic import CreateView, DetailView, UpdateView
from .forms import CustomUserCreationForm, CustomUserUpdateForm
from django.urls import reverse_lazy 
from django.shortcuts import redirect
from django.views import View
from .models import CustomUser
# Create your views here.
class HomeView(View):
    def get(self, request):
        return redirect('article_list') 

class SignupView(CreateView):
    form_class=CustomUserCreationForm
    template_name= 'registration/signup.html'  
    success_url = reverse_lazy('login') 

class Profilview(DetailView):
    model=CustomUser
    template_name='profil_view.html'


# class Profilupdateview(UpdateView):
#     model=CustomUser
#     form_class=CustomUserCreationForm
#     template_name='profil_edit.html'
#     success_url=reverse_lazy('profil_view')

class Profilupdateview(UpdateView):
    model = CustomUser
    form_class = CustomUserUpdateForm
    template_name = 'profil_edit.html'
    
    def get_success_url(self):
        return reverse_lazy('profil_view', kwargs={'pk': self.request.user.pk})

    def get_object(self, queryset=None):
        return self.request.user  # faqat o‘zini tahrirlashi mumkin