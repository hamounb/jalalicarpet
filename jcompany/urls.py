from django.urls import path
from .views import *

app_name = "jcompany"

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('about-us/', AboutUsView.as_view(), name='about-us'),
    path('contact-us/', ContactUsView.as_view(), name='contact-us'),
    path('question/', QuestionView.as_view(), name='question'),
    path('exhibition/', ExhibitionView.as_view(), name='exhibition'),
    path('exhibition/city/<int:cit>/', CityView.as_view(), name='city'),
    path('news/', FooterNewsView.as_view(), name="news"),
]