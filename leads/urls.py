from django.urls import path
from .views import lead_delete, lead_detail, lead_list, lead_create ,lead_update,LeadListView,LeadDetailView,LeadCreateView,LeadUpdateView,LeadDeleteView



app_name="leads"
urlpatterns = [
    path("",LeadListView.as_view(),name="lead"),
    path("<int:pk>",LeadDetailView.as_view(), name="lead_detail"),
    path("<int:pk>/edit",LeadUpdateView.as_view(), name="lead_update"),
    path("<int:pk>/delete",LeadDeleteView.as_view(), name="lead_delete"),
    path("create/",LeadCreateView.as_view(),name="lead_create"),
 ]
