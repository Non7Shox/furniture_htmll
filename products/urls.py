from django.urls import path

from products.views import ProductsListView, ProductsDetailView, add_or_remove

app_name = 'products'

urlpatterns = [
    path('', ProductsListView.as_view(), name='list'),
    path('detail/<int:pk>/', ProductsDetailView.as_view(), name='detail'),
    path('cart/<int:pk>/', add_or_remove, name='add_or_remove'),
]
