import time
import json
import requests

from utils import config_util as cfg
from utils import util




def build_prompt(observation=""):
    """此步骤在dify中进行"""
    pass



def get_communication_history(uid=0):
    """此步骤在dify中进行"""
    pass


def send_request(session: requests.Session, data, uid="0", observation=""):
    url = cfg.gpt_base_url + "/chat-messages"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {cfg.key_gpt_api_key}'
    }
    data = {
        "inputs": {},
        "query": data,
        "response_mode": "streaming",
        "user": f"user_{uid}",
        "conversation_id": uid,
    }
    try:
        if data["response_mode"] == "streaming":
            with session.post(url, json=data, headers=headers, stream=True, timeout=180) as response:
                response.raise_for_status()
                for chunk in response.iter_lines():
                    if not chunk:
                        continue
                    decoded_line = chunk.decode('utf-8').strip()
                    try:
                        message = json.loads(decoded_line)
                        if message["event"] == "message_end":
                            print("收到完整的响应:", message)
                            return message["answer"]
                    except json.JSONDecodeError:
                        print("无法解析的响应行:", decoded_line)
                        return "dify内部错误"
        else:
            response = session.post(url, json=data, headers=headers, timeout=180)
            response.raise_for_status()
            response_data = response.json()
            response_data = response_data["answer"]
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        response_text = "抱歉，我现在太忙了，休息一会，请稍后再试。"
    return response_text



def question(content, uid=0, observation=""):
    start_time = time.time()
    response_text = send_request(requests.Session(), content, uid, observation)
    elapsed_time = time.time() - start_time
    util.log(1, f"接口调用耗时: {elapsed_time:.2f} 秒")
    return response_text


if __name__ == "__main__":
    for _ in range(3):
        query = "爱情是什么"
        response = question(query)
        print("\nThe result is:", response)
