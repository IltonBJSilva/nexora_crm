from django.contrib import admin
from django.urls import path

from core import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("workspace/", views.WorkspaceIndexView.as_view(), name="workspace"),
    path("workspace/<slug:entity_slug>/", views.EntityListView.as_view(), name="entity-list"),
    path("workspace/<slug:entity_slug>/<int:pk>/editar/", views.EntityUpdateView.as_view(), name="entity-update"),
    path("workspace/<slug:entity_slug>/<int:pk>/excluir/", views.EntityDeleteView.as_view(), name="entity-delete"),
]
