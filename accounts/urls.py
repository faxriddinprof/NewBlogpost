from django.urls import path
from .views import SignupView, Profilview, Profilupdateview, LogoutView  

urlpatterns = [
    path('signup/',SignupView.as_view(), name='signup'),
    path('profil/',Profilview.as_view(), name='profil_view'),
    path('profil/edit/', Profilupdateview.as_view(), name='profil_edit'),
    path('logout/', LogoutView.as_view(), name='logout'), 
]   