"""
URL configuration for TradingProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from . import views


urlpatterns = [
    # Path for uploading data and timeframe
    #path('', views.upload_data, name='upload_data'),
    path('', views.upload_data, name='upload_data'),
    path('upload_data', views.upload_data, name='upload_data'),

    # Path for retrieving converted data and JSON download
    path('get_data', views.get_converted_data, name='get_data'),
]
