from django.urls import path
from .views import AgentListView,AgentCreateView,AgentDetailView,AgentUpdateView


app_name='agents'
urlpatterns=[
    path('',AgentListView.as_view(),name='agent_list'),
    path('<int:pk>',AgentDetailView.as_view(),name='agent_detail'),
    path('<int:pk>/update',AgentUpdateView.as_view(),name='agent_update'),
    path('create',AgentCreateView.as_view(),name='agent_create'),
     
    
    
    ] 