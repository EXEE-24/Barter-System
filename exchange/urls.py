from django.urls import path
from . import views

app_name = 'exchange'

urlpatterns = [
    path('proposals/', views.proposal_list, name='proposal_list'),
    path('propose/<int:ad_id>/', views.create_proposal, name='create_proposal'),
    path('proposals/<int:pk>/update/', views.update_proposal, name='update_proposal'),
]