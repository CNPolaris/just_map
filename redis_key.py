GRID_EXPIRED = 60*60

GRID_SHAPE = 'grid'
GRID_PARAMS = 'params'
GRID_ARRAY = 'grid_array'
GRID_LIST = 'grid_list'

BAIDU_GRID_SHAPE = 'baidu_grid'
BAIDU_GRID_PARAMS = 'baidu_params'
BAIDU_GRID_ARRAY = 'baidu_grid_array'
BAIDU_GRID_LIST = 'baidu_grid_list'

BAIDU_GRID_SHAPE2 = 'baidu_grid2'
BAIDU_GRID_PARAMS2 = 'baidu_params2'
BAIDU_GRID_ARRAY2 = 'baidu_grid_array2'
BAIDU_GRID_LIST2 = 'baidu_grid_list2'

BAIDU_GRID_SHAPE3 = 'baidu_grid3'
BAIDU_GRID_PARAMS3 = 'baidu_params3'
BAIDU_GRID_ARRAY3 = 'baidu_grid_array3'
BAIDU_GRID_LIST3 = 'baidu_grid_list3'

from django.core.cache import cache

def format_grid_list(username, map_type):
    return '{0}:{1}:grid_list'.format(username, map_type)

def format_grid_shape(username, map_type):
    return '{0}:{1}:grid_shape'.format(username, map_type)

def format_grid_params(username, map_type):
    return '{0}:{1}:grid_params'.format(username, map_type)

def format_grid_array(username, map_type):
    return '{0}:{1}:grid_array'.format(username, map_type)

def format_grid_accuracy(username, map_type):
    return '{0}:{1}:grid_accuracy'.format(username, map_type)

def format_grid_bounds(username, map_type):
    return '{0}:{1}:grid_bounds'.format(username, map_type)
    
def set_grid(username, map_type, bounds, accuracy, grid_list, grid_array, grid_params):
    cache.set(format_grid_bounds(username, map_type), bounds)
    cache.set(format_grid_accuracy(username, map_type), accuracy)
    cache.set(format_grid_list(username,map_type), grid_list)
    cache.set(format_grid_array(username, map_type), grid_array)
    cache.set(format_grid_params(username, map_type), grid_params)
    
def get_grid(username, map_type):
    
    bounds = cache.get(format_grid_bounds(username, map_type))
    accuracy = cache.get(format_grid_accuracy(username, map_type))
    grid_list = cache.get(format_grid_list(username,map_type))
    grid_array = cache.get(format_grid_array(username, map_type))
    grid_params = cache.get(format_grid_params(username, map_type))
    return bounds, accuracy, grid_list, grid_array,grid_params
            
            
            
            
            
            
def vaild_bounds(username, map_type, bounds):
    key = format_grid_bounds(username, map_type)
    if not cache.has_key(key):
        return False
    elif bounds!=cache.get(key):
        return False
    else:
        return True
    
def valid_accuracy(username, map_type, accuracy):
    key = format_grid_accuracy(username, map_type)
    if not cache.has_key(key):
        return False
    elif accuracy != cache.get(key):
        return False
    else:
        return True
    
def valid_gen(username, map_type):
    grid_list_key = format_grid_list(username, map_type)
    if not cache.has_key(grid_list_key):
        return False
    # grid_shape_key = format_grid_shape(username, map_type)
    # if not cache.has_key(grid_shape_key):
    #     return False
    grid_array_key = format_grid_array(username, map_type)
    if not cache.has_key(grid_array_key):
        return False
    grid_params_key = format_grid_params(username, map_type)
    if not cache.has_key(grid_params_key):
        return False
    
    return True