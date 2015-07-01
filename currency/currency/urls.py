"""currency URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from api import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/currency$', views.CurrencyList.as_view(), name='currency'),
    url(r'^api/currency/(?P<name>([a-zA-Z])+)$', views.CurrencyDetails.as_view(), name='currency-details'),
    url(r'^api/convert/(?P<amount>([0-9.])+)/(?P<from_currency>([a-zA-Z])+)/(?P<to_currency>([a-zA-Z])+)$',
        views.CurrencyConvert.as_view(), name='convert'),
]

