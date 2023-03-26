from django.urls import path
from .views import  LeadListView,LeadDetailView,LeadCreateView,LeadUpdateView,LeadDeleteView,AssignAgentView,CategoryListView,CategoryDetailView,LeadCategroyUpdateView



app_name="leads"
urlpatterns = [
    path("",LeadListView.as_view(),name="lead"),
    path("<int:pk>",LeadDetailView.as_view(), name="lead_detail"),
    path("<int:pk>/edit",LeadUpdateView.as_view(), name="lead_update"),
    path("<int:pk>/delete",LeadDeleteView.as_view(), name="lead_delete"),
    path("create/",LeadCreateView.as_view(),name="lead_create"),
    path("<int:pk>/assign/",AssignAgentView.as_view(),name="assign_agent"),
    path("<int:pk>/category/",LeadCategroyUpdateView.as_view(),name="lead-category-update"),
    path("categories",CategoryListView.as_view(),name="category_list"),
    path("categories/<int:pk>/",CategoryDetailView.as_view(),name="category_detail"),
 ]
