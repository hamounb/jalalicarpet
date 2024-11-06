from django.urls import path

from .views import *

app_name="blog"

urlpatterns = [
    path('', BlogView.as_view(), name='blog'),
    path('details/<int:bid>/', BlogDetailsView.as_view(), name='blog-details'),
]