"""mod_tmrpg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from modtmrpg import views
from modtmrpg.api.MacroKeyBind import api_mkb

urlpatterns = [
    path('', views.index, name='index'),
    path('shop/', views.shop, name='shop'),
    path('shop/<str:status>', views.shop, name='buy_item_success'),
    path('shop/buy/<int:id>', views.buy_item, name='buy_item'),
    path('files/New/', views.new_file, name='new_file'),
    path('files/<str:category>/', views.media_view, name='media_view'),
    path('modsEdit/', views.modsEdit, name='modsEdit'),
    path('modsList/', views.modsList, name='modsList'),
    path('ecoLogs/', views.ecoLogs, name='ecoLogs'),
    path('profile/<str:nick>/', views.profile, name='profile'),
    path('skinfix/<str:nick>/', views.skinfix, name='skinfix'),
    path('api/oc/moders/', views.api_OC_moders, name='api_OC_moders'),
    path('api/oc/config/<str:configName>/', views.api_OC_config, name='api_OC_config'),
    path('get_shop_items/', views.get_shop_items, name='get_shop_items'),
]

apiUrls = [
    path('api/mkb/playtimereport/', api_mkb.api_macrokb_playtimereport, name='api_macrokb_playtimereport'),
    path('api/mkb/getplaytimereport/', api_mkb.api_macrokb_getPlayTimeReport, name='api_macrokb_getPlayTimeReport'),
    path('api/oc/pushplaytimes/', api_mkb.api_macrokb_oc_pushplaytimes, name='api_macrokb_oc_pushplaytimes'),
    ]

[urlpatterns.append(urlpattern) for urlpattern in apiUrls]
