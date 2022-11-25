from django.shortcuts import render
from django.core.cache import cache
import geopandas as gp

from utils.resp import result
from utils.logger import logger
from lib import area_to_grid, gen_grids_array
from redis_key import *
from utils.resp import OK

# Create your views here.
def gen_grids_array_to_redis(request):
    """gen_grids_array_to_redis 栅格矩阵相关初始化接口
    """
    bounds = [119.359038, 32.11255, 119.364167, 32.11883]
    gird_list = []
    if (not cache.has_key(GRID_SHAPE)) | (not cache.has_key(GRID_PARAMS)) | (not cache.has_key(GRID_ARRAY)) | (not cache.has_key(GRID_LIST)):
        grid, params = area_to_grid(bounds)
        if type(grid) == gp.GeoDataFrame:
            grid = grid['geometry'].to_list()
        if type(grid) == gp.GeoSeries:
            grid =  grid.to_list()
        # 每个格子的边界点
        for i in range(len(grid)):
            lng1, lat1, lng2, lat2 = grid[i].bounds
            temp = {
                'lng1': lng1,
                'lat1': lat1,
                'lng2': lng2,
                'lat2': lat2,
                'index': i + 1
            }
            gird_list.append(temp)
        lake_path = '/home/polaris/projects/just_map/static/shape/boundary.shp'
        island_path = '/home/polaris/projects/just_map/static/shape/island.shp'
        grid_array = gen_grids_array(grid, params=params, lake_path=lake_path, island_path=island_path)
        # 设置缓存
        cache.set(GRID_SHAPE, grid, GRID_EXPIRED)
        cache.set(GRID_PARAMS, params, GRID_EXPIRED)
        cache.set(GRID_ARRAY, grid_array, GRID_EXPIRED)
        cache.set(GRID_LIST, gird_list, GRID_EXPIRED)
    else:
        gird = cache.get(GRID_SHAPE)
        params = cache.get(GRID_PARAMS)
        gird_list = cache.get(GRID_LIST)
        grid_array = cache.get(GRID_ARRAY)
        
    return result(OK, message="ok", data=gird_list)

def get_grid_params(request):
    
    params = cache.get('params')
    return result(message='ok',data=params)
