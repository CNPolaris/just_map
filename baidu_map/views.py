from django.shortcuts import render
from django.core.cache import cache
import geopandas as gp

from utils.resp import result
from utils.logger import logger
from lib import area_to_grid, gen_grids_array
from redis_key import *
from utils.resp import OK, format_request

MAP_TYPE = 'baidu'

# Create your views here.
def baidu_gen_array(request):
    bounds = [119.37098775602607,32.11655934651841,119.37609501851392,32.12293903313633]
    gird_list = []
    if (not cache.has_key(BAIDU_GRID_SHAPE)) | (not cache.has_key(BAIDU_GRID_PARAMS)) | (not cache.has_key(BAIDU_GRID_ARRAY)) | (not cache.has_key(BAIDU_GRID_LIST)):
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
        lake_path = '/home/polaris/projects/just_map/static/shape/baidu_lake.shp'
        island_path = '/home/polaris/projects/just_map/static/shape/baidu_island.shp'
        grid_array = gen_grids_array(grid, params=params, lake_path=lake_path, island_path=island_path)
        # 设置缓存
        cache.set(BAIDU_GRID_SHAPE, grid, GRID_EXPIRED)
        cache.set(BAIDU_GRID_PARAMS, params, GRID_EXPIRED)
        cache.set(BAIDU_GRID_ARRAY, grid_array, GRID_EXPIRED)
        cache.set(BAIDU_GRID_LIST, gird_list, GRID_EXPIRED)
    else:
        gird = cache.get(BAIDU_GRID_SHAPE)
        params = cache.get(BAIDU_GRID_PARAMS)
        gird_list = cache.get(BAIDU_GRID_LIST)
        grid_array = cache.get(BAIDU_GRID_ARRAY)
        
    return result(OK, message="栅格化适配百度地图", data=gird_list)


def baidu_gen_array_v2(request):
    bounds = [119.37098775602607,32.11655934651841,119.37609501851392,32.12293903313633]
    grid_list = []
    if (not cache.has_key(BAIDU_GRID_SHAPE2)) | (not cache.has_key(BAIDU_GRID_PARAMS2)) | (not cache.has_key(BAIDU_GRID_ARRAY2)) | (not cache.has_key(BAIDU_GRID_LIST2)):
        grid, params = area_to_grid(bounds)
        if type(grid) == gp.GeoDataFrame:
            grid = grid['geometry'].to_list()
        if type(grid) == gp.GeoSeries:
            grid =  grid.to_list()  
            
        for i in range(len(grid)):
            lng1, lat1, lng2, lat2 = grid[i].bounds
            temp = [
                {'lng':lng1 , 'lat':lat1 },
                {'lng':lng2 , 'lat':lat1 },
                {'lng':lng2 , 'lat':lat2 },
                {'lng':lng1 , 'lat':lat2 }
            ]
            grid_list.append(temp)
        lake_path = '/home/polaris/projects/just_map/static/shape/baidu_lake.shp'
        island_path = '/home/polaris/projects/just_map/static/shape/baidu_island.shp'
        grid_array = gen_grids_array(grid, params=params, lake_path=lake_path, island_path=island_path)

        cache.set(BAIDU_GRID_SHAPE2, grid, GRID_EXPIRED)
        cache.set(BAIDU_GRID_PARAMS2, params, GRID_EXPIRED)
        cache.set(BAIDU_GRID_ARRAY2, grid_array, GRID_EXPIRED)
        cache.set(BAIDU_GRID_LIST2, grid_list, GRID_EXPIRED)
    else:
        grid = cache.get(BAIDU_GRID_SHAPE2)
        params = cache.get(BAIDU_GRID_PARAMS2)
        grid_list = cache.get(BAIDU_GRID_LIST2)
        grid_array = cache.get(BAIDU_GRID_ARRAY2)
        
    return result(OK, '栅格化适配百度地图',grid_list)


def gen_baidu_grid_v3(request):
    bounds = [119.37098775602607,32.11655934651841,119.37609501851392,32.12293903313633]
    grid_list = []
    if (not cache.has_key(BAIDU_GRID_SHAPE3)) | (not cache.has_key(BAIDU_GRID_PARAMS3)) | (not cache.has_key(BAIDU_GRID_ARRAY3)) | (not cache.has_key(BAIDU_GRID_LIST3)):
        grid, params = area_to_grid(bounds)
        if type(grid) == gp.GeoDataFrame:
            grid = grid['geometry'].to_list()
        if type(grid) == gp.GeoSeries:
            grid =  grid.to_list()  
        
        for i in range(len(grid)):
            lng1, lat1, lng2, lat2 = grid[i].bounds
            grid_list.append({
                'geometry': {
                    'type': "Polygon",
                    'coordinates': [
                        [
                            [lng1 , lat1 ],
                            [lng2 , lat1 ],
                            [lng2 , lat2 ],
                            [lng1 , lat2 ]
                        ]
                    ]
                }
            })
        lake_path = '/home/polaris/projects/just_map/static/shape/baidu_lake.shp'
        island_path = '/home/polaris/projects/just_map/static/shape/baidu_island.shp'
        grid_array = gen_grids_array(grid, params=params, lake_path=lake_path, island_path=island_path)

        cache.set(BAIDU_GRID_SHAPE3, grid, GRID_EXPIRED)
        cache.set(BAIDU_GRID_PARAMS3, params, GRID_EXPIRED)
        cache.set(BAIDU_GRID_ARRAY3, grid_array, GRID_EXPIRED)
        cache.set(BAIDU_GRID_LIST3, grid_list, GRID_EXPIRED)
    else:
        grid = cache.get(BAIDU_GRID_SHAPE3)
        params = cache.get(BAIDU_GRID_PARAMS3)
        grid_list = cache.get(BAIDU_GRID_LIST3)
        grid_array = cache.get(BAIDU_GRID_ARRAY3)
    return result(OK, '', grid_list)

def gen_baidu_grid_v4(request):
    temp_user = 'test'
    request = format_request(request)
    bounds = [float(i) for i in request.params.get('bounds')]
    accuracy = float(request.params.get('accuracy'))
    grid_list = []
    if not valid_accuracy(temp_user, MAP_TYPE, accuracy) or not vaild_bounds(temp_user, MAP_TYPE, bounds) or not valid_gen(temp_user, MAP_TYPE):
        grid_shape, grid_params = area_to_grid(bounds, accuracy=accuracy)
        if type(grid_shape) == gp.GeoDataFrame:
            grid_shape = grid_shape['geometry'].to_list()
        if type(grid_shape) == gp.GeoSeries:
            grid_shape =  grid_shape.to_list()  
        
        for i in range(len(grid_shape)):
            lng1, lat1, lng2, lat2 = grid_shape[i].bounds
            grid_list.append({
                'geometry': {
                    'type': "Polygon",
                    'coordinates': [
                        [
                            [lng1 , lat1 ],
                            [lng2 , lat1 ],
                            [lng2 , lat2 ],
                            [lng1 , lat2 ]
                        ]
                    ]
                }
            })
        # lake_path = '/home/polaris/projects/just_map/static/shape/baidu_lake.shp'
        # island_path = '/home/polaris/projects/just_map/static/shape/baidu_island.shp'
        # grid_array = gen_grids_array(grid_shape, params=grid_params, lake_path=lake_path, island_path=island_path)
        grid_array = 1
        set_grid(temp_user, MAP_TYPE, bounds, accuracy, grid_list, grid_array, grid_params)
    else:
        bounds, accuracy, grid_list, grid_array,grid_params = get_grid(temp_user, MAP_TYPE)
    return result(OK, '', grid_list)

def get_path(request):
    lake = []
    
    with open('/home/polaris/projects/just_map/static/data/path.txt') as f:
        lake_data = f.read()
    for xy in lake_data.split(';'):
        y,_,x = xy.partition(',')
        x = float(x.strip())
        y = float(y.strip())
        lake.append({'lng':x, 'lat':y})
    return result(OK, '', lake)