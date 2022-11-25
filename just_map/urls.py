"""map_control URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

from grids import views as grid_api
from baidu_map import views as baidu
import api_path as api

urlpatterns = [
    path('admin/', admin.site.urls),
    path(api.GRID_GEN, grid_api.gen_grids_array_to_redis),
    path(api.GRID_PARAM, grid_api.get_grid_params),
    path(api.BAIDU_GRID_GEN, baidu.baidu_gen_array),
    path(api.BAIDU_GRID_GEN_2, baidu.baidu_gen_array_v2),
    path(api.BAIDU_GRID_GEN_3, baidu.gen_baidu_grid_v3),
    path('api/baidu/v4/grid', baidu.gen_baidu_grid_v4),
    path('api/route', baidu.get_path)    
]
