from qclassifier import *
from qtransfer import *
from qresult import *
import json
import requests

import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8') #改变标准输出的默认编码
'''问答类'''
class ChatBotGraph:
    def __init__(self):
        self.classifier = QuestionClassifier()
        self.parser = QuestionPaser()
        self.searcher = AnswerSearcher()

    def chat_main(self, sent):
        answer = '抱歉，暂时没有相关记载'
        url_base = 'https://api.ownthink.com/bot?appid=40d71776962e06b5ba8a2bb5db206a2a&userid=user&spoken='
        url = url_base + sent
        sess = requests.get(url)
        res_classify = self.classifier.classify(sent)
        if not res_classify:
            answer1 = sess.text
            answer1 = json.loads(answer1)
            answer2 = answer1['data']['info']['text']
            answer = answer2.replace('小思','小艾')
            return answer
        res_sql = self.parser.parser_main(res_classify)
        final_answers = self.searcher.search_main(res_sql)
        if not final_answers:
            answer1 = sess.text
            answer1 = json.loads(answer1)
            answer2 = answer1['data']['info']['text']
            answer = answer2.replace('小思','小艾')
            return answer
        else:
            return '\n'.join(final_answers)

if __name__ == '__main__':
    handler = ChatBotGraph()
    while 1:
        question = input('用户:')
        answer = handler.chat_main(question)
        #answer=answer.replace('\xa0’, ’ ')
        print('ROBOT:', answer)

