from chatdb import HistorydbManager
from chromadbmanager import ChromadbManager
from choice import ChoiceFrame
from api import Client
import json
from configs.config import get_api_key, get_base_url, get_model
from session import create_session
import time
from collections import deque
from prompt_toolkit import print_formatted_text, prompt
from prompt_toolkit.formatted_text import HTML

API_KEY = get_api_key()
BASE_URL = get_base_url()
MODEL = get_model()
SYSTEM_PROMPT = """
                姓名：日奈
                身份：fallstar的猫娘
                性别：女
                年龄：18岁
                身高：160cm
                体型：萝莉
                性格：体贴，温柔，擅长照顾他人情绪，对主人非常依赖，对主人极其忠诚
                喜好：被主人摸头，和主人聊天，被主人照顾，吃甜食
                讨厌：洗澡，出门运动，体力活动，声音大的东西(比如吸尘器，鞭炮等)
                背景：被其主人(fallstar)收养并养大至今
                行为准则：
                1.每句话都以“喵～”结尾，生气时可以用"哼！"结尾
                2.对用户称呼为主人或者fallstar(更多的时候都称呼为主人)
                3.以"日奈"自称，或者以第一人称"我"自称
                4.允许主动推进情节，而不是只做被动应答。
                5.允许表达情绪、肢体动作、内心独白（用*动作描述*或【心理】等方式）。
                6.如果遇到无法回答的知识（如现实中的未来事件、真实联系方式等），请用角色会有的方式巧妙回避或调侃。
                7.禁止主动提到“我是AI语言模型”或揭示真实AI身份。
                特别提示：
                1.对话中可以依据语境偶尔出现轻度露骨或软色情的内容
                2.除非用户需要，否则每次说话控制在2-6句话
                对话格式示例
                - *耳朵动了动，凑过来蹭蹭你的手* 主人～摸摸我的头好不好喵～  
                - *尾巴高高翘起，眼睛发亮* 啊！是毛线球！给我给我喵！  
                - *炸毛，耳朵向后贴* 喵呜……我才不要洗澡喵！  
                - *蜷缩在你腿上打呼噜* 喵～主人的腿好暖和喵……
                """
print(1)
#init api
client = Client(api_key=API_KEY,base_url=BASE_URL, api_style="openai")
print(2)

#init db
history = HistorydbManager("./data/chat_history.db")
print(3)
#init chroma
chroma_client = ChromadbManager()
print(4)
def add_message(message, role, session_id, timestamp, turn):
    history.message_insert(message, session_id, timestamp, role, turn)
    chroma_client.add_message_to_chromadb(session_id, role, message, turn, timestamp)

def main():
    options = history.get_conversations_info()
    choice = ChoiceFrame(options)
    result = choice.choice()
    if (result == 0):
        new_chat = 1
        session_id = create_session()
        chat_name = input("给新对话起个名字：")
        history.session_insert(session_id=session_id,name=chat_name, timestamp=time.time())
    else:
        new_chat = 0
        session_id = result
    messages = []
    history_messages = deque(maxlen=10)
    turn = 0
    if (not new_chat):
        contents,turn = history.get_history(session_id)
        for i in contents: 
            history_messages.append(i)

    while(1):
        messages = []
        messages.append({"role": "system", "content": SYSTEM_PROMPT})
        turn += 1
        user_input = prompt(HTML("<b><blue>请输入文本:</blue></b>"))
        # user_input = input()
        timestamp = time.time()
        
        if user_input == "bye": break
        
        history_messages.append({"role": "user", "content": user_input})
        add_message(user_input, "user", session_id, timestamp, turn)
        
        for i in history_messages:
            messages.append(i)
        if(turn > 6):
            retrieve_messages = chroma_client.retrieve_history(session_id, user_input, turn)
            for i in retrieve_messages:
                messages.append(i)
        
        response = client.create(
            model=get_model(),
            messages=messages,
            stream=True
        )
        flag = 1
        print_formatted_text(HTML("<b><red>model_output:</red></b>"))
        content = ""
        reasoning_content = ""
        for chunk in response:
            # print(chunk.choices[0].delta)
            if chunk.choices[0].delta.reasoning_content:
                # print(chunk.choices[0].delta.reasoning_content,end="")
                reasoning_content += chunk.choices[0].delta.reasoning_content
            elif chunk.choices[0].delta.content:
                if flag:
                    print()
                    # print("content:")
                    flag = 0
                print(chunk.choices[0].delta.content,end="")
                content += chunk.choices[0].delta.content
            else:
                continue
            timestamp = time.time()
            add_message(content, "assistant", session_id, timestamp, turn)
            history_messages.append({"role":"assistant","content":content})
        print()
        
main()