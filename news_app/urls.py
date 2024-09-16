from django.urls import path
from .views import get_news_list, get_news_detail
from .views import HomePageView, ContactPageView
from .views import LocalNewsView, ForeignNewsView
from .views import TechNewsView, SportNewsView

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('news/', get_news_list, name='get_news_list'),
    path('news/<slug:news>/', get_news_detail, name="get_news_detail"),
    path('contact-us/', ContactPageView.as_view(), name="contact_page"),
    path('local_news/', LocalNewsView.as_view(), name="local_news"),
    path('foreign_news/', ForeignNewsView.as_view(), name="foreign_news"),
    path('tech_news/', TechNewsView.as_view(), name="tech_news"),
    path('sport_news/', SportNewsView.as_view(), name="sport_news"),
]
