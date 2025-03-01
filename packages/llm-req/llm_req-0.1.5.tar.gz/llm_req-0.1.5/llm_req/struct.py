from typing import List, Literal, Optional, Union, Any,Dict, get_type_hints
from types import MethodType
import time
import json
import os
import inspect

class BaseModel(object):
    """
    auto convert to json and dict, inspect all fields
    """

    def __init__(self, **kwargs):
        _args = get_type_hints(self.__class__)

        for k,type_k in _args.items():
            if not hasattr(self.__class__, k) and kwargs.get(k) is None:
                if hasattr(type_k,"__origin__") and type_k.__origin__ is not Union:
                    raise ValueError(f"{k} is required")

            val = kwargs.get(k, None)
            if hasattr(type_k, '__args__'):
            # 获取Optional类型中的实际类型参数
                actual_type = type_k.__args__[0]
                
                if hasattr(actual_type, '__origin__') and actual_type.__origin__ is Union:
                    # print("rogin :",actual_type.__origin__)
                    for tp in actual_type.__args__:
                        if isinstance( tp, type):
                            # print(tp)
                            try:
                                actual_type = tp
                                if isinstance(val, dict):
                                    val = actual_type.from_dict(val)
                                elif isinstance(val, list):
                                    val = [actual_type.from_dict(v) for v in val]
                                setattr(self, k, val)
                            except Exception as e:
                                # print(e)
                                continue
                
                elif  isinstance(actual_type, type) and issubclass(actual_type, BaseModel):
                    if isinstance(val, dict):
                        val = actual_type.from_dict(val)
                    elif isinstance(val, list):
                        # print( "list :",val)
                        val = [actual_type.from_dict(v) for v in val]
                    
                    # else:
                    #     raise ValueError(f"{k} must be a dict or list of dict you are: {val}")

                setattr(self, k, val)
            elif issubclass(type_k, BaseModel):
                val = type_k.from_dict(val)
                setattr(self, k, val)
            else:
                if k not in kwargs:
                    if hasattr(self.__class__, k):
                        val = getattr(self.__class__, k)
                    else:
                        raise ValueError(f"{k} is required")
                setattr(self, k, val)

    @property
    def json(self):
        return json.dumps(self.dict())
    

    def __repr__(self):
        return json.dumps(self.dict(), indent=2)
    
    # @classmethod
    # def _members(cls):
    #     _args = {}
    #     _must = {}
    #     _ops = {}
    #     for name,val in inspect.getmembers(cls):
    #         if name == '__annotations__':
    #             _args = val
    #             break

    #     for k,v in _args.items():
    #         if 'Optional' in str(v) :
    #             _ops[k] = True
    #         else:
    #             _args[k] = True
    #     for n in _args:
    #         if not hasattr(cls, n):
    #             _must[n] = True
    #     return _must, _args, _ops
    
    def dict(self):
        d = {}
        # qs = 
        for name in get_type_hints(self):
            val = getattr(self, name)
            if isinstance(val, MethodType):
                continue
            elif val is None:
                continue
            elif isinstance(val, BaseModel):
                val = val.dict()
            elif isinstance(val, list):
                val = [v.dict() if isinstance(v, BaseModel) else v for v in val]
            
            d[name] = val
        return d

    @classmethod
    def from_json(cls, data: str):
        d = json.loads(data)
        return cls.from_dict(d)
    
    @classmethod
    def from_dict(cls, data: dict):
        if isinstance(data, BaseModel):
            return data
        return cls(**data)

class ModelCard(BaseModel):
    id: str
    object: str = "model"
    created: int = int(time.time())
    owned_by: str = "owner"
    root: Optional[str] = None
    parent: Optional[str] = None
    path: Optional[str] = None
    permission: Optional[list] = None
    task: Optional[str] = ""

class Document(BaseModel):
    id: str = None
    page_content: str
    metadata: Optional[Dict]  = {}

class NoneRequest(BaseModel):
    id: str = "None"

class DocsRequest(BaseModel):
    id: str
    docs: Union[List[str], List[Document]] 
    stream: Optional[bool] = False

class ModelList(BaseModel):
    object: str = "list"
    data: List[ModelCard] = []


class FunctionCallResponse(BaseModel):
    name: Optional[str] = None
    arguments: Optional[str] = None


class MessageRequest(BaseModel):
    messages: List[str]
    stream: Optional[bool] = False

class EmbedingResponse(BaseModel):
    len: Optional[int]
    id: str = "embeding_zh"
    data: Any
    used: float


class ModelCallRequest(BaseModel):
    id: str
    messages: List[str]
    stream: Optional[bool]
    

class ModelCallResponse(BaseModel):
    id: str
    data: Union[List[int],List[str], List[dict], List[List[dict]], dict]
    used: float
    error: Optional[str]



class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system", "function","observation"]
    content: str = None
    name: Optional[str] = None
    tools: Optional[Dict] = None
    function_call: Optional[FunctionCallResponse] = None

class ToolCallResponse(BaseModel):
    id: str = None
    type: str
    function: FunctionCallResponse

class DeltaMessage(BaseModel):
    role: Optional[Literal["user", "assistant", "system"]] = None
    content: Optional[str] = None
    function_call: Optional[FunctionCallResponse] = None
    tool_calls: Optional[List[ToolCallResponse]] = None


class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    temperature: Optional[float] = 0.8
    top_p: Optional[float] = 0.8
    max_tokens: Optional[int] = None
    image: Optional[str] = None
    stream: Optional[bool] = False
    functions: Optional[Union[dict, List[dict]]] = None
    tools: Optional[Union[dict, List[dict]]] = None
    # Additional parameters
    repetition_penalty: Optional[float] = 1.1


class KnowledgeCompletionRequest(BaseModel):
    knowledge_id:str
    model: str
    messages: List[ChatMessage]
    temperature: Optional[float] = 0.8
    top_p: Optional[float] = 0.8
    top_k: Optional[int] = 7
    max_tokens: Optional[int] = None
    stream: Optional[bool] = False
    functions: Optional[Union[dict, List[dict]]] = None
    repetition_penalty: Optional[float] = 1.1


class KnowDocs(BaseModel):
    knowledge_id:str
    docs: List[str]

class ChatCompletionResponseChoice(BaseModel):
    index: int
    message: ChatMessage
    finish_reason: Literal["stop", "length", "function_call"]


class ChatCompletionResponseStreamChoice(BaseModel):
    index: int
    delta: DeltaMessage
    finish_reason: Optional[Literal["stop", "length", "function_call"]]


class UsageInfo(BaseModel):
    prompt_tokens: int = 0
    total_tokens: int = 0
    completion_tokens: Optional[int] = 0

class MachineInfo(BaseModel):
    gpu: int = 0
    memory_use: Optional[float]
    gpu_usage: Optional[List[Dict]]
    loaded_models: Optional[ModelList]

class ChatCompletionResponse(BaseModel):
    model: str
    object: Literal["chat.completion", "chat.completion.chunk"]
    choices: List[Union[ChatCompletionResponseChoice, ChatCompletionResponseStreamChoice]]
    created: Optional[int] =  int(time.time())
    usage: Optional[UsageInfo] = None



class KnowCompletionResponse(BaseModel):
    model: str
    object: Literal["chat.completion", "chat.completion.chunk"]
    choices: List[Union[ChatCompletionResponseChoice, ChatCompletionResponseStreamChoice]]
    sources: List[Document] = []
    created: Optional[int] = int(time.time())
    usage: Optional[UsageInfo] = None

class ClearRequest(BaseModel):
    ids: List[str]




class VoiceCallResponse(BaseModel):
    id: str
    data: Union[List[int],List[str], List[dict], List[List[dict]], dict]
    used: float = 0.1
    error: Optional[str]
    speed: float = 0.7

class VoiceCallRequest(BaseModel):
    id: str
    data: Union[List[int],List[str], List[dict], List[List[dict]], dict]
    used: float = 0.1
    error: Optional[str] = "no error"
    speed: float = 0.7
    stream: bool = True
