import os
import base64
from typing import Generator
from .struct import VoiceCallRequest,VoiceCallResponse
import requests
import json
import io
import gzip

def decompress(data):
    decompressed_file = io.BytesIO(data)
    # 使用gzip的GzipFile类来解压缩数据
    decompressed_data = None
    with gzip.GzipFile(fileobj=decompressed_file, mode='rb') as f:
        decompressed_data = f.read()
    return decompressed_data
class Voice:
    def __init__(self, remote_host, id="small", speed=0.9):
        self.remote_host = remote_host
        self.id = id
        self.speed = speed
    
    def v2t(self, file_or_data):
        rq = VoiceCallRequest(id=self.id, used=0.9, data=[], error="no error")
        if isinstance(file_or_data, bytes):
            rq.data.append(base64.b64encode(file_or_data).decode())
            
        elif os.path.exists(file_or_data):
            
            with open(file_or_data, 'rb') as fp:
                rq.data.append(base64.b64encode(fp.read()).decode())
        if len(rq.data) > 0:
            res = self._send(rq)
            return res
    
    def t2v(self, text):
        rq = VoiceCallRequest(id="melo", used=0.9,data=[text], speed=self.speed, error="no error")
        res = self._send_t(rq)
        for i in res:
            yield i

    def t2v_file(self, text, dir):
        for no,res in enumerate(self.t2v(text)):
            q = os.urandom(16).hex() + "-"+str(no)
            name = os.path.join(dir, f"{q}.mp3")
            if len(res.data) > 0:
                with open(name, 'wb') as fp:
                    data = res.data[0].encode('utf-8')
                    data = base64.b64decode(data)
                    data = decompress(data)
                    fp.write(data)
                    yield name

    def _send_t(self, rq:VoiceCallRequest)-> Generator[VoiceCallResponse]:
        url = f"http://{self.remote_host}:15001/v1/voice/t2v"
        data = rq.dict()
        response = requests.post(url, json=data, stream=True)
        if response.status_code == 200:    
            for line in response.iter_lines():
                if line:
                    
                    decoded_line = line.decode('utf-8')[6:]
                    try:
                        if decoded_line.strip():
                            response_json = json.loads(decoded_line.strip())
                            yield VoiceCallResponse.from_dict(response_json)
                    except Exception as e:
                        print(response.content)
                        print(e)
                        pass
        else:
            print(response.content)
            

    def _send(self, rq:VoiceCallRequest)-> VoiceCallResponse:
        url = f"http://{self.remote_host}:15001/v1/voice/v2t"
        data = rq.dict()
        response = requests.post(url, json=data)
        return VoiceCallResponse.from_dict(response.json())


    def play(self, file:str):
        try:
            import wave
            import pydub
            import pyaudio
            import time
            if file.endswith(".mp3"):
                filet = file.replace(".mp3", ".wav")
                pydub.AudioSegment.from_mp3(file).export(filet, format="wav")
                with wave.open(filet, 'rb') as wf:
                    # Define callback for playback (1)
                    def callback(in_data, frame_count, time_info, status):
                        data = wf.readframes(frame_count)
                        # If len(data) is less than requested frame_count, PyAudio automatically
                        # assumes the stream is finished, and the stream stops.
                        return (data, pyaudio.paContinue)

                    # Instantiate PyAudio and initialize PortAudio system resources (2)
                    p = pyaudio.PyAudio()

                    # Open stream using callback (3)
                    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                                    channels=wf.getnchannels(),
                                    rate=wf.getframerate(),
                                    output=True,
                                    stream_callback=callback)

                    # Wait for stream to finish (4)
                    while stream.is_active():
                        time.sleep(0.1)
                    # Close the stream (5)
                    stream.close()

                    # Release PortAudio system resources (6)
                    p.terminate()
            elif file.endswith(".wav"):
                with wave.open(file, 'rb') as wf:
                    # Define callback for playback (1)
                    def callback(in_data, frame_count, time_info, status):
                        data = wf.readframes(frame_count)
                        # If len(data) is less than requested frame_count, PyAudio automatically
                        # assumes the stream is finished, and the stream stops.
                        return (data, pyaudio.paContinue)

                    # Instantiate PyAudio and initialize PortAudio system resources (2)
                    p = pyaudio.PyAudio()

                    # Open stream using callback (3)
                    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                                    channels=wf.getnchannels(),
                                    rate=wf.getframerate(),
                                    output=True,
                                    stream_callback=callback)

                    # Wait for stream to finish (4)
                    while stream.is_active():
                        time.sleep(0.1)
                    # Close the stream (5)
                    stream.close()

                    # Release PortAudio system resources (6)
                    p.terminate()
        except Exception as e:
            raise e
    
    def try_install_extension(sefl):
        os.system("pip install pyaudio wave -i https://pypi.tuna.tsinghua.edu.cn/simple")

    def listen(self, chat_llm=None, speak=False):
        try:
            import wave
            import sys
            import pyaudio
            import tempfile
            import threading
            import queue
            running = True
            def _play(e:queue.Queue):
                print("Start Speaker")
                while running:
                    f = e.get()
                    print("play:", f)
                    self.play(f)
            
            q = queue.Queue()
            t =None
            if speak:
                t = threading.Thread(target=_play, args=(q,))
                t.start()


            CHUNK = 1024
            FORMAT = pyaudio.paInt16
            CHANNELS = 1 if sys.platform == 'darwin' else 2
            RATE = 44100
            RECORD_SECONDS = 5
            tmp_name = os.urandom(16).hex() + ".wav"
            d = tempfile.mkdtemp()
            tmpFile = os.path.join(d, tmp_name)
            with wave.open(tmpFile, 'wb') as wf:
                p = pyaudio.PyAudio()
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(p.get_sample_size(FORMAT))
                wf.setframerate(RATE)

                stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True)

                print('Recording...')
                for _ in range(0, RATE // CHUNK * RECORD_SECONDS):
                    wf.writeframes(stream.read(CHUNK))
                print('Done')

                stream.close()
                p.terminate()

            res = self.v2t(tmpFile)
            if chat_llm is not None:
                for data in res.data:
                    new_i = ""
                    for i in chat_llm(data["text"]):
                        # print(i["new"], )
                        if not speak:
                            print(i["new"], end="", flush=True)
                        else:

                            new_i += i["new"]
                            print(i["new"], end="", flush=True)
                            if new_i.count("\n") > 1:
                                fs = new_i.split("\n")
                                send_res = "\n".join(fs[:3])
                                new_i = "\n".join(fs[3:])

                                for f in self.t2v_file(send_res, d):
                                    q.put(f)
                    if speak:
                        send_res = new_i
                        for f in self.t2v_file(send_res, d):
                            q.put(f)
            else:
                return res
            if speak:
                if q.empty():
                    running = False
                
            if t is not None:
                t.join()
                
        except Exception as e:

            raise e
