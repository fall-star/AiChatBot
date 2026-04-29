from openai import OpenAI
from configs import config
import time
import chromadb
from chromadb.utils import embedding_functions

SYSTEM_PROMPT = "你是一个ai助手"
#init openai
model_client = OpenAI(
    api_key=config.api_key,
    base_url=config.base_url
)

# init chroma
# chroma_client = chromadb.PersistentClient("./chroma_db")
# ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="BAAI/bge-small-zh-v1.5")
# collection = chroma_client.get_or_create_collection("my_docs", embedding_function=ef)

def main():
    messages = []
    messages.append({"role":"system","content":SYSTEM_PROMPT})
    while(1):
        user_input = input()
        if(user_input == "bye"): break
        messages.append({"role":"user","content":user_input})
        response = model_client.chat.completions.create(
            model=config.model,
            messages=messages,
            stream=True,
            # extra_body={"thinking": {"type": "disabled"}},
        )
        flag = 1
        print("model_output:")
        content = ""
        reasoning_content = ""
        for chunk in response:
            # print(chunk.choices[0].delta)
            if chunk.choices[0].delta.reasoning_content:
                print(chunk.choices[0].delta.reasoning_content,end="")
                reasoning_content += chunk.choices[0].delta.reasoning_content
            elif chunk.choices[0].delta.content:
                if flag:
                    print()
                    print("content:")
                    flag = 0
                print(chunk.choices[0].delta.content,end="")
                content += chunk.choices[0].delta.content
                messages.append({"role":"system","content":content})
            else:
                continue
        print()
        # print(f"model_output:{content}")

main()
    