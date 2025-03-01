
import argparse
from .llm import LLM
from loguru import logger
parser = argparse.ArgumentParser(usage="call llm use remote's host [api based open-ai]")
parser.add_argument("-u","--remote-host", help="default to initialize a projet in current dir")
parser.add_argument("-m","--model",default="/root/.cache/glm-4-9b-chat", help="default to initialize a projet in current dir")


def main():
    args = parser.parse_args()
    if args.remote_host:
        llm = LLM(args.remote_host)
        llm.id = args.model    
        while 1:
            try:
                q = input("type 'q' exit >>")
                if q == "q":
                    break
                if q.strip() == "":continue
                llm.out(q)
                print()
            except Exception as e:
                logger.error(e)
            except KeyboardInterrupt:
                break


if __name__ == "__main__":
    main()
