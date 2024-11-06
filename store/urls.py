from django.urls import path
from .views import *

app_name = "store"

urlpatterns = [
    path('category/', CategoryView.as_view(), name='category-list'),
    path('category/<int:cid>/', CategoryProductsView.as_view(), name='category-products'),
    path('products/all/', AllProductsView.as_view(), name='all-products'),
    path('products/details/<str:code>/', ProductDetailsView.as_view(), name='product-details'),
    path('cart/add/<int:pid>/', CartAddView.as_view(), name="cartadd"),
    path('cart/remove/<int:pid>/', CartRemoveView.as_view(), name="cartremove"),
    path('cart/details/', CartDetailsView.as_view(), name="cartdetails"),
    path('products/tag/<int:id>/', TagsView.as_view(), name="tag-products"),
    # path('price/', PriceUpdateView.as_view(), name='price-update'),
    path('images/delete/', ImagesDeleteView.as_view(), name='images-delete'),
]