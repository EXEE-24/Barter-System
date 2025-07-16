from django.urls import path
from . import views

app_name = 'ads'

urlpatterns = [
    path('', views.ad_list, name='ad_list'),
    path('create/', views.ad_create, name='ad_create'),
    path('<int:pk>/', views.ad_detail, name='ad_detail'),
    path('<int:pk>/update/', views.ad_update, name='ad_update'),
    path('<int:pk>/delete/', views.ad_delete, name='ad_delete'),
    path('<int:ad_id>/propose/', views.proposal_create, name='proposal_create'),
    path('proposals/<int:pk>/', views.proposal_detail, name='proposal_detail'),
]