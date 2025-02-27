from typing import get_origin
try:
    from typing import  Annotated
except :
    pass
import inspect
import traceback
import copy

_TOOL_HOOKS = {}
_TOOL_DESCRIPTIONS = {}

def as_tool(func: callable):
    tool_name = func.__name__
    tool_description = inspect.getdoc(func).strip()
    python_params = inspect.signature(func).parameters
    tool_params = {}
    requireds = []
    for name, param in python_params.items():
        annotation = param.annotation
        if annotation is inspect.Parameter.empty:
            raise TypeError(f"Parameter `{name}` missing type annotation")
        try:
            if get_origin(annotation) != Annotated:
                raise TypeError(f"Annotation type for `{name}` must be typing.Annotated")
        except TypeError as e:
            raise e
        except Exception as e:
            print(e)
        typ, (description, required) = annotation.__origin__, annotation.__metadata__
        # if typ.__name__
        typ: str = str(typ) #  typ.__name__
        if not isinstance(description, str):
            raise TypeError(f"Description for `{name}` must be a string")
        if not isinstance(required, bool):
            raise TypeError(f"Required for `{name}` must be a bool")

        tool_params[name]= {
            
            "description": description,
            "type": typ,
            
        }
        if required:
            requireds.append(name)

    tool_def = {
        "name": tool_name,
        "description": tool_description,
        "parameters": {
            "type":"object",
            "properties": tool_params,
            "required": requireds
        }
    }

    # print("[registered tool] " + pformat(tool_def))
    _TOOL_HOOKS[tool_name] = func
    _TOOL_DESCRIPTIONS[tool_name] = tool_def
    return func

def unregister_tool(tool_name:str) -> bool:
    if tool_name in _TOOL_HOOKS:
        del _TOOL_HOOKS[tool_name]
    if tool_name in _TOOL_DESCRIPTIONS:
        del _TOOL_DESCRIPTIONS[tool_name]
    return True

def dispatch_tool(tool_name: str, tool_params: dict) -> str:
    if tool_name not in _TOOL_HOOKS:
        return f"Tool `{tool_name}` not found. Please use a provided tool."
    tool_call = _TOOL_HOOKS[tool_name]
    try:
        ret = tool_call(**tool_params)  
    except:
        ret = traceback.format_exc()
    return str(ret)

def get_tools() -> dict:
    return copy.deepcopy(_TOOL_DESCRIPTIONS)


try:

    @as_tool
    def get_weather(
        city_name: Annotated[str, 'The name of the city to be queried', True],
        ) -> str:
        """
        Get the current weather for `city_name`
        """

        if not isinstance(city_name, str):
            raise TypeError("City name must be a string")

        key_selection = {
            "current_condition": ["temp_C", "FeelsLikeC", "humidity", "weatherDesc",  "observation_time"],
        }
        import requests
        try:
            resp = requests.get(f"https://wttr.in/{city_name}?format=j1")
            resp.raise_for_status()
            resp = resp.json()
            ret = {k: {_v: resp[k][0][_v] for _v in v} for k, v in key_selection.items()}
        except:
            import traceback
            ret = "Error encountered while fetching weather data!\n" + traceback.format_exc() 

        return str(ret)
    
    @as_tool
    def get_loc(
        ip_address: Annotated[str, 'The IP address. if set None will use current machine\'s ip', False] = None,
        ) -> dict:
        """
        通过ip获取当前的地理位置信息
        """
        import requests
        import bs4
        if ip_address == None:
            res = requests.get("http://cip.cc").text
            rr = {}
            for l in res.strip().split("\n"):
                if ":" in l:
                    fs = l.split(":")
                    rr[fs[0].strip()] = fs[1].strip()
        else:
            res = requests.get("http://cip.cc/"+ip_address).text
            res = bs4.BeautifulSoup(res, 'html.parser').text
            rr = {}
            for l in res.strip().split("\n"):
                if ":" in l:
                    fs = l.split(":")
                    rr[fs[0].strip()] = fs[1].strip()
        return rr
    
    @as_tool
    def speaker(
        msg: Annotated[str, 'The message to be spoken.', True],
        ):
        """
        调用本地的语音库播放 msg
        """
        import tempfile
        from llm_req import Voice
        v = Voice(remote_host="xx.xxx.xx.xx")
        tmp = tempfile.mkdtemp()
        
        for f in v.t2v_file(msg, tmp):
            v.play(f)
        return "执行完毕"
    
    @as_tool
    def get_my_machine_info(
        network: Annotated[bool, "If set True will return network information.", False] = False,
        ):
        """
        获取本机的信息, 默认会获取 用户目录, 以及各种env信息,当network设置为True时会顺便获取网络信息
        """
        import os
        import sys
        if network:
            import psutil
            return str(psutil.net_if_stats())
        dd = {}
        dd["HOME"] = os.environ.get("HOME", "")
        dd["PWD"] = os.environ.get("PWD", "")
        dd["PATH"] = os.environ.get("PATH", "")
        dd["PLATFORM"] = sys.platform
        return str(dd)

    @as_tool
    def find_file(
        key: Annotated[str, 'The key in file name.', True],
        root: Annotated[str, 'The root directory to search.', True],
        ) -> str:
        """
        查找指定目录下文件名包含指定key的文件.
        """
        import os
        import glob
        import pathlib
        ret = []
        for root, ds , fs in os.walk(pathlib.Path(root).expanduser()):
            for f in fs:
                if key in f:
                    path = os.path.join(root, f)
                    ret.append(path)
        return str(ret)
    
    
    

except Exception as e:
    print(e)



