from django.urls import path
from .views import SignupView, Profilview, Profilupdateview

urlpatterns = [
    path('signup/',SignupView.as_view(), name='signup'),
    path('profil/<int:pk>/',Profilview.as_view(), name='profil_view'),
    path('profil/edit/', Profilupdateview.as_view(), name='profil_edit')
]   