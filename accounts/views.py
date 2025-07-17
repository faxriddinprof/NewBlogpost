from django.views.generic import CreateView, DetailView, UpdateView
from django.urls import reverse_lazy 
from django.shortcuts import redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages  # ✅ Messages import qilindi
from .forms import CustomUserCreationForm, CustomUserUpdateForm
from .models import CustomUser
from django.contrib.auth.views import LogoutView as DjangoLogoutView

# 🏠 Bosh sahifaga yo‘naltiruvchi view
class HomeView(View):
    def get(self, request):
        return redirect('article_list') 

# 📝 Ro‘yxatdan o‘tish
class SignupView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'  
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, "✅ Muvaffaqiyatli ro'yxatdan o'tdingiz! Endi tizimga kiring.")
        return super().form_valid(form)
    
 # 👤 Profilni ko‘rish — request.user asosida, pk yo‘q
class Profilview(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'profil_view.html'
    context_object_name = 'profile_user'

    def get_object(self, queryset=None):
        return self.request.user  # har doim hozirgi foydalanuvchini qaytaramiz



# ✏ Profilni tahrirlash
class Profilupdateview(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserUpdateForm
    template_name = 'profil_edit.html'
    
    def get_object(self, queryset=None):
        return self.request.user  # faqat o‘zini tahrirlashi mumkin

    def form_valid(self, form):
        messages.success(self.request, "✅ Profil muvaffaqiyatli yangilandi.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profil_view')


# THIS IS LOGOUT CLASS 

class LogoutView(DjangoLogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "👋 Tizimdan chiqdingiz. Qaytib kelishingizni kutamiz!")
        return super().dispatch(request, *args, **kwargs)
