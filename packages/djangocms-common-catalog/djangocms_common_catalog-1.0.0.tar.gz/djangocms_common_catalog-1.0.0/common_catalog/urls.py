from django.urls import path

from .views import CatalogItemView, CatalogListView

urlpatterns = [
    path("<int:pk>/", CatalogItemView.as_view(), name="item"),
    path("", CatalogListView.as_view(), name="list"),
]
