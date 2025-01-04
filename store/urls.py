from django.urls import path
from .views import *

app_name = "store"

urlpatterns = [
    path('category/<str:pc>/', CategoryView.as_view(), name='category-list'),
    path('products/category/<int:cid>/', CategoryProductsView.as_view(), name='category-products'),
    path('products/category/<int:cid>/visit/', CategoryProductsVisitedView.as_view(), name='category-products-visited'),
    path('products/category/<int:cid>/on-sale/', CategoryProductsSaleView.as_view(), name='category-products-sale'),
    path('products/category/<int:cid>/high-to-low/', CategoryProductsHighView.as_view(), name='category-products-high'),
    path('products/category/<int:cid>/low-to-high/', CategoryProductsLowView.as_view(), name='category-products-low'),
    path('products/all/', AllProductsView.as_view(), name='all-products'),
    path('products/details/<str:code>/', ProductDetailsView.as_view(), name='product-details'),
    path('cart/add/<int:pid>/', CartAddView.as_view(), name="cartadd"),
    path('cart/remove/<int:pid>/', CartRemoveView.as_view(), name="cartremove"),
    path('cart/details/', CartDetailsView.as_view(), name="cartdetails"),
    path('products/tag/<int:id>/', TagsView.as_view(), name="tag-products"),
    # path('price/', PriceUpdateView.as_view(), name='price-update'),
    path('images/delete/', ImagesDeleteView.as_view(), name='images-delete'),
    path('search/', HeaderSearchView.as_view(), name="header-search")
]