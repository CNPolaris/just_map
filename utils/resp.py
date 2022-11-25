from django.http import JsonResponse,HttpResponse
import json
# 自定义状态码
ERROR = 0
OK = 1
PARAMS_ERROR = 2
UN_AUTH = 3
METHOD = 4
# 定义统一的 json 字符串返回格式
def result(code=OK, message="", data=None, kwargs=None):
    json_dict = {"code": code, "message": message, "data": data}
    # isinstance(object对象, 类型):判断是否数据xx类型
    if kwargs and isinstance(kwargs, dict) and kwargs.keys():
        json_dict.update(kwargs)
    return JsonResponse(json_dict) 

def format_request(request):
    if request.method == 'GET':
        request.params = request.GET
    elif request.method in ['POST', 'PUT', 'DELETE']:
        request.params = json.loads(request.body)
    return request