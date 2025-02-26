from inspect import signature
from fastapi import APIRouter, FastAPI 
from fastapi.params import Query,Body,Header
from fastapi.responses import StreamingResponse
from fastapi.routing import APIRoute
from pydantic import BaseModel
from pydantic_core import PydanticUndefined

from bilibili.utils.data_tool import to_sse
from rich import print
class InfoRouter():
    def __init__(self,app:FastAPI):
        self.app = app
        self.router = APIRouter()
        self.register_router()
    def register_router(self): 
        @self.router.get("/info",tags=["注册API info"])
        def _info():
            res = {
                    "profile":{
                        "name": "ylz_bilibili",
                        "icon": "图标",
                        "title": "bilibili视频大纲解析",
                        "version": "0.1.6",
                        "author": "youht",
                        "describe": "bilibili视频大纲解析"
                    },
                    "api": []
                    # "api":{
                    #     "method": "GET",
                    #     "url": "/v1/parse_video",
                    #     "query":[{
                    #         "name": "video_url",
                    #         "title": "video的bvid码",
                    #         "type": "string",
                    #         "require": True,
                    #         "describe": "可以传入一个或多个视频rul或视频id,如果多个视频请用`,`分隔",
                    #         "defaultValue": "",
                    #     }],        
                    # }
                }
        
            routes_info = []
            for route in self.app.routes:
                if isinstance(route, APIRoute):
                    #if route.path.startswith(("/v1/parse_video")):
                    if not route.path.startswith(("/docs", "/redoc", "/openapi.json","/info")):
                        route_info = self.get_route_parameters(route)
                        routes_info.append(route_info)
            res["api"] = routes_info
            print("res=",res)
            return res

    def get_model_fields(self,model:BaseModel):
        """
        获取 Pydantic 模型的字段信息。
        """
        fields_info = []
        for field_name, field in model.model_fields.items():
            field_info = {
                "name": field_name,
                "title": field_name.title(),
                "type": field.annotation.__name__,
                "require": field.is_required(),
                "describe": field.description,
                "defaultValue": None if field.default is PydanticUndefined else field.default,
                "enumDefines":[]
            }
            fields_info.append(field_info)
        return fields_info

    def get_route_parameters(self,route:APIRoute):
        """
        获取路由的参数信息，包括路径参数、查询参数和 Pydantic 模型字段。
        """
        route_info = {
            "method": list(route.methods)[0],
            "url": route.path,
            "headers":[],
            "query": [],
            "body": []
        }

        # 获取路由的签名信息
        sig = signature(route.endpoint)
        for param_name, param in sig.parameters.items():
            if param.annotation == param.empty:
                param_type = "Any"
            else:
                param_type = param.annotation

            if param.default is not param.empty:
                print(param.default,type(param.default),isinstance(param.default,Query))
                if isinstance(param.default,Query):
                    route_info["query"].append({
                        "name": param_name,
                        "title": param.default.title,
                        "type": param_type.__name__,
                        "require": param.default.is_required(),
                        "describe": param.default.description,
                        "defaultValue": None if param.default.default is PydanticUndefined else param.default.default,
                        "enumDefines":[]
                    })
                elif isinstance(param.default,Header):
                    route_info["headers"].append({
                        "name": param_name,
                        "title": param.default.title,
                        "type": param_type.__name__,
                        "require": param.default.is_required(),
                        "describe": param.default.description,
                        "defaultValue": None if param.default.default is PydanticUndefined else param.default.default,
                        "enumDefines":[]
                    })
                else:
                    route_info["query"].append({
                        "name": param_name,
                        "title": "?",
                        "type": param_type.__name__,
                        "require": True,
                        "describe": "??",
                        "defaultValue": param.default,
                        "enumDefines":[]
                    })
            elif issubclass(param_type, BaseModel):
                route_info["body"].append(
                    self.get_model_fields(param_type)
                )

        return route_info
