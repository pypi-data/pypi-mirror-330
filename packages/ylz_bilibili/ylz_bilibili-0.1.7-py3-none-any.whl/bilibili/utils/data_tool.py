from typing import Union
import json
def to_sse(obj:Union[dict,str])->str:
    if isinstance(obj,dict):
        obj_sse = f"data: ```json\n{json.dumps(obj,ensure_ascii=False)}\n```\n\n"
    else:
        obj_sse = f"data: ```json\n{str(obj)}\n```\n\n"
    return obj_sse
