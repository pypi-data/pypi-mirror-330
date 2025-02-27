
from hashlib import md5
import time
import requests
from .struct import MessageRequest
import json


class Embeding:

    def __init__(self, remote_host: str, token=""):
        self.remote_host = remote_host
        self.use_code = False
        self.token = token
        self.functions = None
    
    def embed_documents_remote(self, texts):
        uri = f"https://{self.remote_host}/v1/embeddings"
        # user_id = md5(time.asctime().encode()).hexdigest()
        try:
            m = MessageRequest(messages=texts, stream=True)
            ss = []
            for i in R(uri, m, use_stream=True, token=self.token):
                ss += i["data"]
            return ss
        except Exception as e:
            raise e
            # print(e)
            # import ipdb;ipdb.set_trace()
    
    def embed_query_remote(self, text):
        uri = f"https://{self.remote_host}/v1/embeddings"
        # user_id = md5(time.asctime().encode()).hexdigest()
        # TODAY = datetime.datetime.now()
        # PASSWORD = "ADSFADSGADSHDAFHDSG@#%!@#T%DSAGADSHDFAGSY@#%@!#^%@#$Y^#$TYDGVDFSGDS!@$!@$" + f"{TODAY.year}-{TODAY.month}"
        # ws.send(json.dumps({"user_id":user_id, "password":PASSWORD}))
        # # time.sleep(0.5)
        # res = ws.recv()
        # if res != "ok":
        #     print(colored("[info]:","yellow") ,res)
        #     raise Exception("password error")
        
        # data = json.dumps({"embed_documents":texts})
        try:
            m = MessageRequest(messages=[text], stream=True)
            ss = []
            for i in R(uri, m, use_stream=True,token=self.token):
                ss += i["data"]
            return ss[0]
        except Exception as e:
            print(e)
            import ipdb;ipdb.set_trace()

    def embed_documents(self, texts):
        assert self.remote_host is not None
        return self.embed_documents_remote(texts)
        
    def embed_query(self, text: str):
        assert self.remote_host is not None
        return self.embed_query_remote(text)
        
    
    def __call__(self, texts):
        if isinstance(texts, str):
            return self.embed_query(texts)
        return self.embed_documents(texts)




def R(uri, object=None, method='post',use_stream=False,token="", **datas):
    data = {}
    data.update(datas)
    o = None
    if object is not None:
        o = object.dict()
        if "stream" in o:
            # print("Set Stream:",use_stream)
            object.stream = use_stream
        o = object.dict()
        data.update(o)
    H = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token,
    }
    if method == "post":
        response = requests.post(uri, headers=H, json=data, stream=use_stream, verify=False)
    else:
        response = requests.get(uri, json=data, stream=use_stream,verify=False)
    if response.status_code == 200:
        if use_stream:
            # 处理流式响应
            if "messages" in o:
                T = (len(object.messages) // 50) + 1
                if uri.endswith("embeddings"):
                    T = (len(object.messages) // 100) + 1
                # bar = tqdm.tqdm(total=T,desc=" + deal data")
                # bar.leave = False
                for line in response.iter_lines():
                    if line:
                        if line[:6] == b": ping" and line[6] != b"{":continue
                        decoded_line = line.decode('utf-8')[6:].strip()
                        if decoded_line:
                            try:
                                response_json = json.loads(decoded_line)
                                # bar.update(1)
                                yield response_json
                            except Exception as e:
                                print("Special Token:", e, len(line), line)
                # bar.clear()
                # bar.close()
        else:
            # 处理非流式响应
            decoded_line = response.json()
            yield decoded_line
    else:
        print("Error:", response.status_code)
        print("Response:", response.content)
        return None


