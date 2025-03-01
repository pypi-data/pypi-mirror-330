import json
from io import StringIO
from typing  import Iterable
from loguru import logger
import pathlib
from hashlib import md5
from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures import as_completed
import os
import warnings
import pathlib
warnings.filterwarnings("ignore", message=".*certificate.*")
AGENT_CACHE = pathlib.Path("~/.cache/agents").expanduser()
if not AGENT_CACHE.exists():
    AGENT_CACHE.mkdir(parents=True)

def list_agent() -> Iterable[str]:
    fs = [os.path.basename(x).replace(".json", "") for x in os.listdir(str(AGENT_CACHE)) if x.endswith(".json")]
    for f in fs:
        if "Agent" in f:
            yield f

AGS = {
    
}

def load_agent(name):
    d = os.path.join(AGENT_CACHE, name+".json")
    if os.path.exists(d):
        with open(d, 'r') as f:
            da = json.loads(f.read())
            tpcls:Agent = AGS.get(da.get('type', Agent))
            a:Agent = tpcls(target=da.get('target',''))
            a._data = da.get('data',[])
            a.set_point(*da['points'])
            a.batch_size = da.get('batch_size', 10)
            a.threads = da.get('threads', 1)
            a.set_example(da.get('example',''))
            a.set_llm(da.get('model', ''), da.get('model_api',''))
            return a

TEST_DATA = [
{"id":"1","name":"John","age":30,"city":"New York"},
{"id":"2","name":"Jane","age":25,"city":"Chicago"},
{"id":"3","name":"Bob","age":35,"city":"Los Angeles"},
{"id":"4","name":"Alice","age":28,"city":"San Francisco"},
{"id":"5","name":"Mike","age":32,"city":"Boston"},
{"id":"6","name":"Emily","age":27,"city":"Seattle"},
{"id":"7","name":"David","age":31,"city":"Houston"},
{"id":"8","name":"Sarah","age":29,"city":"Dallas"},
{"id":"9","name":"Chris","age":33,"city":"Miami"},
{"id":"10","name":"Linda","age":26,"city":"Atlanta"},
{"id":"11","name":"Tom","age":34,"city":"Philadelphia"},
{"id":"12","name":"Karen","age":30,"city":"Phoenix"},
{"id":"13","name":"Mark","age":31,"city":"San Diego"},
{"id":"14","name":"Jessica","age":32,"city":"Denver"},
{"id":"15","name":"Andrew","age":29,"city":"Detroit"},
{"id":"16","name":"Megan","age":28,"city":"Austin"},
{"id":"17","name":"Daniel","age":27,"city":"San Jose"},
{"id":"18","name":"Laura","age":26,"city":"Minneapolis"},
{"id":"19","name":"Steven","age":33,"city":"Columbus"},
{"id":"20","name":"Amy","age":30,"city":"Charlotte"},
{"id":"21","name":"Brian","age":31,"city":"Indianapolis"},
{"id":"22","name":"Rachel","age":32,"city":"Nashville"},
{"id":"23","name":"Jason","age":28,"city":"Louisville"},
{"id":"24","name":"Kim","age":27,"city":"Portland"},
{"id":"25","name":"Ryan","age":26,"city":"San Francisco"},
{"id":"26","name":"Emily","age":27,"city":"Seattle"},
{"id":"27","name":"David","age":31,"city":"Houston"},
{"id":"28","name":"Sarah","age":29,"city":"Dallas"},
{"id":"29","name":"Chris","age":30,"city":"Miami"},
{"id":"30","name":"Jennifer","age":32,"city":"Boston"},
{"id":"31","name":"Kevin","age":33,"city":"Philadelphia"},
{"id":"32","name":"Melissa","age":28,"city":"Atlanta"},
{"id":"33","name":"Eric","age":27,"city":"San Antonio"},
{"id":"34","name":"Jessica","age":26,"city":"Detroit"},
{"id":"35","name":"Andrew","age":31,"city":"San Diego"},
{"id":"36","name":"Amanda","age":30,"city":"Denver"},
{"id":"37","name":"Nicholas","age":29,"city":"Chicago"},
{"id":"38","name":"Elizabeth","age":32,"city":"Phoenix"},
{"id":"39","name":"Jacob","age":28,"city":"Austin"},
{"id":"40","name":"Samantha","age":27,"city":"San Jose"},
{"id":"41","name":"Matthew","age":26,"city":"San Diego"},
{"id":"42","name":"Ashley","age":31,"city":"San Francisco"},
{"id":"43","name":"Joshua","age":30,"city":"Seattle"},
{"id":"44","name":"Olivia","age":29,"city":"Houston"},
{"id":"45","name":"Daniel","age":32,"city":"Dallas"},
{"id":"46","name":"Emma","age":28,"city":"Miami"},
{"id":"47","name":"William","age":27,"city":"Boston"},
{"id":"48","name":"Sophia","age":26,"city":"Philadelphia"},
{"id":"49","name":"Joseph","age":31,"city":"Atlanta"},
{"id":"50","name":"Mia","age":30,"city":"San Antonio"}
]


class BaseAgent:
    BASE = """{DESC}
{EXAMPLE}
{OUTPUT_FORMAT}
{DATA}
"""
    def __init__(self, *point, target="", format=""):
        self._example = ""
        self._point = point
        self._target = target
        self._output_format = format
        self._data = []
        self._data_title = "# fowllow is data:"
        self._example_title = "# example:"
        self._output_format_title = "# output use this format:"

    @property
    def description(self):
        base = f"# {self.desc}:\n" 
        for no,i in enumerate(self.point):
            base += f" {no+1}. {i}.\n"
        return base
    
    @property
    def example(self):
        return self._example
    @property
    def output_format(self):
        return self._output_format
    @property
    def point(self):
        return self._point
    
    def set_point(self, *point):
        if len(self._point) == 0:
            self._point = point
        else:
            d = list(self.point)
            for i in point:
                if i not in self._point:
                    d.append(i)
            self._point = tuple(d)
        return self
    
    def set_example(self, example):
        self._example = example
        return self

    def set_target(self, target):
        self._target = target
        return self

    def points(self, *point):
        return self.set_point(*point)
    def argu(self, *args):
        return self.points(*args)
    def conditions(self, condition):
        return self.points(condition)
    def set_condition(self, *condition):
        return self.points(condition)

    @property
    def desc(self):
        return self._target
    
    def input(self, *items):
        self._data = items
        return self
    
    def __add__(self, data):
        if isinstance(data, (list, tuple)):
            for i in data:
                self._data.append(i)
            return self
        elif isinstance(data, str):
            self._data.append(data)
            return self
        else:
            raise ValueError("data must be string or iterable")
    
    

            

    def __lshift__(self, data):
        if isinstance(data, (list, tuple)):
            self._data = []
            for i in data:
                self._data.append(i)
            return self
        elif isinstance(data, str):
            self._data = []
            self._data.append(data)
            return self
        else:
            raise ValueError("data must be string or iterable")
    
    def convertstr(self,item, use_json=False):
        if isinstance(item, dict):
            if use_json:
                return json.dumps(item)
            p = ""
            for k in sorted(item.keys()):
                p += f"\n{k}: {item[k]} "
            return p
        else:
            return str(item)

        
    def __truediv__(self, data):
        if isinstance(data, str):
            return self.input(data)
        elif isinstance(data, Iterable):
            return self.input(*data)
        else:
            raise ValueError("data must be string or iterable")

    def update(self, agent):
        if agent._example:
            self._example = agent._example
        
        if agent._output_format:
            self._output_format = agent._output_format
        
        if agent._target:
            self._target = agent._target
        
        if agent._point and len(agent._point) > 0:
            self._point = agent._point

        if agent._data and len(agent._data) > 0:
            self._data = agent._data
        
        if agent._data_title:
            self._data_title = agent._data_title
        
        if agent._output_format_title:
            self._output_format_title = agent._output_format_title
        
        if agent._example_title:
            self._example_title = agent._example_title

        return self
    
    def data_batch(self, batch_size=20):
        data = []
        for i in self._data:
            
            data.append(i)
            # logger.info(f"data size: {len(data)} bsize: {batch_size} {type(batch_size)}")
            if len(data) == batch_size:
                yield data
                data = []
        if len(data) > 0:
            yield data


    def __str__(self):
        data = ""
        if self._data and len(self._data) > 0:
            data = "\n\n".join([self.convertstr(i) for i in next(self.data_batch(batch_size=5))])
        if data.strip() != "":
            data = self._data_title +"........" +"\n"+ data
        
        _example = self.example
        if _example != "":
            _example = self._example_title +"\n"+ self._example

        _output_format = self.output_format
        if self._output_format != "":
            _output_format = self._output_format_title +"\n"+ self.output_format
        
        return self.BASE.format(DESC=self.description, EXAMPLE=_example, OUTPUT_FORMAT=_output_format, DATA=data).strip()
    
    def output(self, batch_size=10):
        for items in self.data_batch(batch_size):
            logger.info(f"items: {len(items)} size: {batch_size}")
            data = "\n\n".join([self.convertstr(i) for i in items])
            if data.strip() != "":
                data = self._data_title +"\n"+ data
            
            _example = self.example
            if _example != "":
                _example = self._example_title +"\n"+ self._example

            _output_format = self.output_format
            if self._output_format != "":
                _output_format = self._output_format_title +"\n"+ self.output_format
            
            yield self.BASE.format(DESC=self.description, EXAMPLE=_example, OUTPUT_FORMAT=_output_format, DATA=data).strip()

    def __repr__(self):
        return self.__str__()

class Agent(BaseAgent):
    """
    最基础算子
    可以调整的参数有：
    - batch_size: 每次输出数据的数量，默认为 10
    - threads: 是否支持并发多请求，默认为 1
    - target: 算子的目的描述，          必须填写
    - points: 对于描述的限制条件或者要求

如何构造一个Agent的任务:
1. 初始化描述，包括target和points， batch_size和threads
```python
a = Agent(target="找到数据中是是存在某个条件的数据")
# # 设置要定要求
a.set_points("要求条件是年龄大于20", "要求条件是性别是男")
print(a)

~ # 找到数据中是是存在某个条件的数据:
~    1. 要求条件是年龄大于20.
~    2. 要求条件是性别是男.

2. 初始化数据，包括data和
# exmaple datas:
DATA = [
    {"name": "张三", "age": 18, "gender": "男"},
    {"name": "李四", "age": 20, "gender": "女"},
    {"name": "王五", "age": 22, "gender": "男"},
]
a = a | DATA
#3. 初始化输出，包括output，默认为空: 如给任务的添加一个JsonAgent格式化输出：
b = a | JsonAgent     
```
    """
    batch_size = 10
    threads = 1


    def __init__(self, *args,batch_size=10,threads=1, **kwargs):
        super().__init__(*args, **kwargs)
        self.batch_size = batch_size
        self.threads = threads
        self._model = ""
        self._model_api = ""

    def __rshift__(self, other):
        if isinstance(other, BaseAgent):
            return other.update(self)
        elif isinstance(other, type):
            other_instance = other()
            return other_instance.update(self)
        else:
            raise TypeError("Right operand must be an instance of BaseAgent or a subclass of BaseAgent")

    def update(self, other):
        o = super().update(other)
        if isinstance(o, Agent):
            o.batch_size = self.batch_size
            o.threads = self.threads
        return o

    def to_dict(self):
        return {

            'type': self.__class__.__name__,
            'target': self._target,
            'batch_size': self.batch_size,
            'threads': self.threads,
            'data': self._data,
            'points': self._point,
            'example': self._example,
            'model': self._model,
            'model_api': self._model_api
        }
    
    def set_llm(self, model, model_api):
        self._model = model
        self._model_api = model_api
        return self
   

    def save(self, name):
        d = os.path.join(AGENT_CACHE, name +'.json')
        with open(d, 'w') as f:
            f.write(json.dumps({
                'name': name,
                'type' : self.__class__.__name__,
                'target': self._target,
                'data': self._data,
                'points': self._point,
                'example': self._example,
                'batch_size': self.batch_size,
                'threads': self.threads,
                'model': self._model,
                'model_api': self._model_api
            }))
        return self

    def __or__(self, other):
        if isinstance(other, BaseAgent):
            return other.update(self)
        elif isinstance(other, type):
            other_instance = other()
            return other_instance.update(self)
        elif isinstance(other, (list, tuple,)):
            for i in other:
                self._data.append(i)
            return self
        else:
            if hasattr(other, "stream") and hasattr(other, "out"):
                return self.output_to_llm(other)
            raise TypeError("Right operand must be an instance of BaseAgent or a subclass of BaseAgent")

    def output_to_llm(self, llm, datas=[], each_clear=False):
        batch_size = self.batch_size
        if len(datas) == 0:
            datas = self.output(batch_size=batch_size)
        if self.threads <= 1:
            for o in datas:
                strIO = StringIO()
                llm.out(o, out=strIO)
                
                llm.clear_history()
                strIO.seek(0)
                yield strIO.read()
            
        else:
            exe = ThreadPoolExecutor(max_workers=self.threads)
            fus = []
            def _oo(ollm, o):
                strIO = StringIO()
                llm = ollm.copy_llm()
                llm.clear_history()
                llm.out(o, out=strIO)
                strIO.seek(0)
                return strIO.read()

            for o in datas:                
                fus.append(exe.submit(_oo, llm, o))
                # llm.out(o, out=strIO)
            for fut in as_completed(fus):
                batch_res = fut.result()
                yield batch_res
        
class ExcelDataAgent(Agent):
    """
    Excel格式输入算子， 继承至Agent
       通过这个Agent可以额外处理pd格式的data
     
    """
    def __or__(self, other):
        try:
            import pandas as pd
            if isinstance(other, pd.DataFrame):
                for no,row in enumerate(other.iloc):
                    item = {}
                    for key in other:
                        item[key] = str(row[key])
                    if "id" not in item:
                        item["id"] = no
                    self._data.append(item)
                return self
            elif isinstance(other, str) and os.path.exists(other) and (other.endswith(".xlsx") or other.endswith(".xls") or other.endswith(".csv")):
                if other.endswith(".xlsx") or other.endswith(".xls"):
                    df = pd.read_excel(other)
                else:
                    df = pd.read_csv(other)
                for no,row in enumerate(df.iloc):
                    item = {}
                    for key in df:
                        item[key] = str(row[key])
                    if "id" not in item:
                        item["id"] = no
                    self._data.append(item)
                return self
            else:
                return super().__or__(other)
        except Exception as e:
            raise Exception("pandas not found, please install pandas or:",e)

class JsonAgent(Agent):
    """
    Json格式输出算子， 继承至Agent
    可以调整的参数有：
    -  Agent 的基础参数: 参考 Agent的描述

    - key: 对每个输入的数据data使用key作为其唯一标识,默认为 "id". 例如data: {"id": 1, "name": "Tom"}， 即会取 data["id"]作为其唯一标识
    - type: 输出数据的类型，默认为 "chooses"，即输出为选择列表，例如：[{"id": 1, "name": "Tom"}, {"id": 2, "name": "Jerry"}]
    - save: 是否保存日志文件，默认为 False
    - log_root: 日志文件保存的根目录，默认为 ~/.llm_req_log

如何构造一个Agent的任务:
```python
# 1. 初始化描述，包括target和points， batch_size和multi_req  
a = Agent(target="找到数据中是是存在某个条件的数据")
2. 初始化数据，包括data和
# exmaple datas:
DATA = [
    {"name": "张三", "age": 18, "gender": "男"},
    {"name": "李四", "age": 20, "gender": "女"},
    {"name": "王五", "age": 22, "gender": "男"},
]
a = a | DATA

3. 初始化输出，包括output，默认为空: 如给任务的添加一个JsonAgent格式化输出：
b = a | JsonAgent 
4. 执行任务，包括执行器，默认为None: 如给任务添加一个执行器：
llm = LLM(remote_ip="xx.xxx.xxx.xx:xx")
batch_result_generator = b | llm
for batch_result in batch_result_generator:
    for item_dict in  batch_result:
        print(item_dict)
```
    """
    type:str = "chooses"
    key:str = "id"
    log_root = pathlib.Path("~/.llm_req_log").expanduser()

    def __init__(self, *args,key="id",save=False,type="chooses", log_root=None,  format="use this JSON format to output: ", **kwargs):
        super().__init__(*args, format=format, **kwargs)
        self.key = key
        self.log = save
        if log_root is not None:
            self.log_root = log_root
        self.type = type

    def update(self, other):
        o = super().update(other)
        if isinstance(o, JsonAgent):
            o.key = self.key
            o.type = self.type
            o.log = self.log
            o.log_root = self.log_root
        return o
    
    def convertstr(self, item):
        return super().convertstr(item, use_json=True)

    @property
    def output_format(self):
        if self._data is None or len(self._data) == 0:
            return ""
        base = ""
        if self.key in self._data[0]:
            if self.type == "choose" or self.type == "select" or self.type == "pick" or self.type == "choose one":
                base = '{'+f'"{self.key}": "here is your {self.key}"'+'} , ps: only can output one item'
            elif self.type == "chooses" or self.type == "selects" or self.type == "picks" or self.type == "choose all":
                base = f'[%s"{self.key}": "here is your {self.key}"%s, %s"{self.key}": "here is another item\'s {self.key}"%s....]' % ("{" , "}", "{", "}")
        return self._output_format + base + "\n"
    

    def id(self, base_name:str):
        return md5(base_name.encode()).hexdigest()
    
    def output_to_llm(self, llm):
        erros = []
        if self.log:
            if isinstance(self.log_root, str):
                self.log_root = pathlib.Path(self.log_root).expanduser()
            assert isinstance(self.log_root, pathlib.Path)
            id = self.id(self._target)
            
            root = self.log_root  / id
            root.mkdir(parents=True, exist_ok=True)
            input_num = 0
            answer_num = 0
        try:
            f = None
            if self.log:
                f = open(str(root/ "raw.log"), "a+")
                for input in self._data:
                    f.write("\n"+json.dumps({"tp":"input", "raw":input}))
                    input_num += 1
            for output in super().output_to_llm(llm):
                try:
                    item_str = output.split("```json")[1].split("```")[0]
                    o = json.loads(item_str)
                    if self.log:
                        f.write("\n"+json.dumps({"tp":"output", "raw":o}))
                        answer_num += 1
                    yield o
                except Exception as e:
                    try:
                        
                        item_str = output.split("```")[1].split("```")[0].strip()
                        o = json.loads(item_str)
                        if self.log:
                            f.write("\n"+json.dumps({"tp":"output", "raw":o}))
                            answer_num += 1
                        yield o
                    except Exception as e:
                        logger.error(str(e) + "  >> '"+output+"'")
                        erros.append(output)
            if len(erros) > 0:
                for e in super().output_to_llm(llm, datas=erros):
                    try:
                        item_str = e.split("```json")[1].split("```")[0]
                        o = json.loads(item_str)
                        if self.log:
                            f.write("\n"+json.dumps({"tp":"output", "raw":o}))
                            answer_num += 1
                    except Exception as e:
                        try:
                            item_str = output.split("```")[1].split("```")[0]
                            o = json.loads(item_str.strip())
                            if self.log:
                                f.write("\n"+json.dumps({"tp":"output", "raw":o}))
                                answer_num += 1
                        except Exception as e:
                            logger.error(str(e) + "  >> "+output)
                            erros.append(output)
        finally:
            if self.log:
                f.close()

class ClassifyAgent(Agent):
    """
    ClassifyAgent 
    分类算子
    - .... Agent's argument:..... ( see detail in Agent's __doc__)
    
    - labels: list of classifiers's categories

如何构造分类任务
```python
#
# datas:
datas = [
    {"id": 1, "name": "张三", "city": "A城市"},
    {"id": 2, "name": "李四", "city": "B城市"},
    {"id": 3, "name": "王五", "city": "C城市"},
    {"id": 4, "name": "赵六", "city": "A城市"},
    {"id": 5, "name": "钱七", "city": "B城市"},
    {"id": 6, "name": "孙八", "city": "C城市"},
    {"id": 7, "name": "周九", "city": "A城市"},
    {"id": 8, "name": "吴十", "city": "B城市"},
    {"id": 9, "name": "郑十一", "city": "C城市"},
    {"id": 10, "name": "王十二", "city": "A城市"},
    {"id": 11, "name": "李十三", "city": "B城市"},
    {"id": 12, "name": "张十四", "city": "C城市"},
    {"id": 13, "name": "赵十五", "city": "A城市"},
    {"id": 14, "name": "钱十六", "city": "B城市"},
    {"id": 15, "name": "孙十七", "city": "C城市"},
    {"id": 16, "name": "周十八", "city": "A城市"},
    {"id": 17, "name": "吴十九", "city": "B城市"},
    {"id": 18, "name": "郑二十", "city": "C城市"},
    {"id": 19, "name": "王二十一", "city": "A城市"},
    {"id": 20, "name": "李二十二", "city": "B城市"},
    {"id": 21, "name": "张二十三", "city": "C城市"},
    {"id": 22, "name": "赵二十四", "city": "A城市"},
    {"id": 23, "name": "钱二十五", "city": "B城市"},
    {"id": 24, "name": "孙二十六", "city": "C城市"},
    {"id": 25, "name": "周二十七", "city": "A城市"},
    {"id": 26, "name": "吴二十八", "city": "B城市"},
    {"id": 27, "name": "郑二十九", "city": "C城市"},
    {"id": 28, "name": "王三十", "city": "A城市"},
    {"id": 29, "name": "李三十一", "city": "B城市"},
    {"id": 30, "name": "张三十二", "city": "C城市"},
    {"id": 31, "name": "赵三十三", "city": "A城市"},
]


task = ClassifyAgent("好人", "坏人", "不太坏的人") # 设置要分类的类别
task  |= datas # 加载数据

# 设置输出格式要求
# save : 是否保存结果
# threads: 并发是否多请求
task |= JsonAgent(threads=3, save=True) 

# 设置要定要求
task.set_point("好人住在A城市", "坏人住在B城市", "不太坏的人住在C城市")
for batch in task | JsonAgent(threads=3, save=True):
    print(batch)
```
    """
    def __init__(self, *labels, format="", **kwargs):
        # assert len(labels) > 0
        target = "classify each piece of data."
        points = [
            "Please classify the following data into one of the following categories: " + ",".join([f"\"{i}\"" for i in labels]),
            "Each piece of data's category can not be empty."
        ]
        super().__init__(*points, target=target, format=format, **kwargs)
    

    def __or__(self, other):
        if isinstance(other, (list,tuple)):
            if isinstance(other[0], (str,int)):
                points = [
                    "Please classify the following data into one of the following categories: " + ",".join([f"\"{i}\"" for i in other]),
                    "Each piece of data's category can not be empty."
                ]
                self.set_point(*points)
                return self
            else:
                return super().__or__(other)
            
        else:
            return super().__or__(other)



class MapReduceAgent(Agent):
    def output_to_llm(self, llm, datas=[]):
        parts = []
        for part in super().output_to_llm(llm, datas, each_clear=True):

            print(part)
            parts.append(part)
        reduce_prompt = ""
        for no,part in enumerate(parts):
            reduce_prompt += f"\n\n总结{no+1}：\n{part}"
        reduce_prompt = """根据以上的多个总结，请将它们合并成一个总结，合并后的总结需要包含以下内容："""
        reduce_prompt += "\n\n".join(self._point)
        
        def _oo(ollm, o):
            strIO = StringIO()
            lm = ollm.copy_llm()
            lm.clear_history()
            lm.out(o, out=strIO)
            strIO.seek(0)
            return strIO.read()
        return _oo(llm, reduce_prompt)
    

AGS["Agent"] = Agent
AGS["MapReduceAgent"] = MapReduceAgent
AGS["JsonAgent"] = JsonAgent
AGS["ExcelDataAgent"] = ExcelDataAgent
