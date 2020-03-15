#-*-coding:utf-8-*-
import textwrap
import os
import pymongo

class MedicalGraph:
    def __init__(self):
        self.conn = pymongo.MongoClient()
        self.db = self.conn['medical']
        self.col = self.db['data']
        self.col2 = self.db['symptom']
        self.col3 = self.db['drug']
        self.path="disease"
        self.symptom_path="symptom"
        self.drug_path = "drug"


    def collect_medical(self):
        flag_name = ["name", "desc", "cause", "treatment", "prevent", "symptoms", "drug", "check"]
        for root, dirs, files in os.walk(self.path):
            for file in files:
                print(file)
                data = {}
                flag = [0, 0, 0, 0, 0, 0, 0, 0]  # name desc cause treatment prevent symptoms drug check
                content = ""
                f = open("disease/"+file, encoding='utf-8')
                for line in f:
                    if str(line.split("\n")[0])=="============"and 1 in flag:
                        label=flag_name[flag.index(1)]
                        content=content[0:-1]
                        data[label]=content
                        flag[flag.index(1)]=0
                        content=""
                    if 1 in flag and str(line.split("\n")[0])!="":
                        s=str(line.split("\n")[0])
                        content+=textwrap.fill(s, 60)+"\n"
                    if str(line.split("\n")[0])=="名称":
                        flag[0]=1
                        continue
                    if str(line.split("\n")[0])=="概述":
                        flag[1]=1
                        continue
                    if str(line.split("\n")[0])=="病因":
                        flag[2]=1
                        continue
                    if str(line.split("\n")[0])=="治疗":
                        flag[3]=1
                        continue
                    if str(line.split("\n")[0])=="预防":
                        flag[4]=1
                        continue
                    if str(line.split("\n")[0])=="症状":
                        flag[5]=1
                        continue
                    if str(line.split("\n")[0])=="药品":
                        flag[6]=1
                        continue
                    if str(line.split("\n")[0])=="检查":
                        flag[7]=1
                        continue
                print(data)
                self.col.insert(data)

    def collect_symptom(self):
        for root, dirs, files in os.walk(self.symptom_path):
            for file in files:
                print(file)
                data = {}
                flag_name = ["name", "desc",]
                flag = [0, 0]  # name desc cause treatment prevent symptoms drug check
                content = ""
                f = open(self.symptom_path+"/"+file)
                for line in f:
                    if str(line.split("\n")[0])=="============"and 1 in flag:
                        label=flag_name[flag.index(1)]
                        content=content[0:-1]
                        data[label]=content
                        flag[flag.index(1)]=0
                        content=""
                    if 1 in flag and str(line.split("\n")[0])!="":
                        s=str(line.split("\n")[0])
                        content+=textwrap.fill(s, 60)+"\n"
                    if str(line.split("\n")[0])=="名称":
                        flag[0]=1
                        continue
                    if str(line.split("\n")[0])=="概述":
                        flag[1]=1
                        continue

                print(data)
                self.col2.insert(data)


    def collect_drug(self):
        for root, dirs, files in os.walk(self.drug_path):
            for file in files:
                print(file)
                data = {}
                flag_name = ["name", "use","adapt","uneffect","forbid","attention"]
                flag = [0,0,0,0,0,0]  # "name", "use","adapt","uneffect","forbid","attention"
                content = ""
                f = open(self.drug_path+"/"+file)
                for line in f:
                    if str(line.split("\n")[0])=="============"and 1 in flag:
                        label=flag_name[flag.index(1)]
                        content=content[0:-1]
                        data[label]=content
                        flag[flag.index(1)]=0
                        content=""
                    if 1 in flag and str(line.split("\n")[0])!="":
                        s=str(line.split("\n")[0])
                        content+=textwrap.fill(s, 60)+"\n"
                    if str(line.split("\n")[0])=="名称":
                        flag[0]=1
                        continue
                    if str(line.split("\n")[0])=="用法用量":
                        flag[1]=1
                        continue
                    if str(line.split("\n")[0])=="适应症":
                        flag[2]=1
                        continue
                    if str(line.split("\n")[0])=="不良反应":
                        flag[3]=1
                        continue
                    if str(line.split("\n")[0])=="禁忌":
                        flag[4]=1
                        continue
                    if str(line.split("\n")[0])=="注意事项":
                        flag[5]=1
                        continue


                print(data)
                self.col3.insert(data)


if __name__ == '__main__':
    handler = MedicalGraph()
    handler.collect_drug()
