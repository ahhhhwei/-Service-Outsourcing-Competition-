import requests
import json

class QABot:
    def __init__(self, token):
        self.url = 'https://keyue.cloud.baidu.com/online/core/v5/stream/query'
        self.headers = {
            'token': token,
            'Content-Type': 'application/json'
        }
        self.session_id = None

    def send_query(self, query):
        data = {
            "queryText": query,
            "sessionId": self.session_id
        }

        response = requests.post(self.url, headers=self.headers, json=data, stream=True)
        final_answer = ""

        # 检查状态码
        if response.status_code == 200:
            try:
                for line in response.iter_lines():
                    if line.startswith(b'data:'):
                        data_json_str = line.decode('utf-8')[5:]
                        data_json = json.loads(data_json_str)
                        # 检查状态是否为'done'
                        if 'answer' in data_json:
                            for message in data_json['answer']:
                                final_answer += message['reply']['text']
                                break  # 结束循环
            except json.JSONDecodeError as e:
                print("JSON Decode Error:", e)
                return None
        else:
            print("Response Text:", response.text)  # 输出响应文本
            return None
        return final_answer


    def start_session(self):
        response = self.send_query('')

        if response is not None:
            self.session_id = response['sessionId']

    def ask(self, question):
        response = self.send_query(question)
        if response != "":
            return response
        else:
            return "Sorry, I couldn't understand your question."

# 使用示例
bot = QABot('6a6748e5-2407-4d97-965f-ee1ea59db7f9')
# bot.start_session()

while True:
    question = input("Ask me a question: ")
    print(type(question))
    answer = bot.ask(question)
    print("Answer:", answer)
