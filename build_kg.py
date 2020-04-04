import os
import re
import json
from py2neo import Graph,Node


class MedicalGraph:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.disease_path = os.path.join(cur_dir, 'data/Disease.json')
        self.drug_path = os.path.join(cur_dir, 'data/Drug.json')
        self.symptom_path = os.path.join(cur_dir, 'data/Symptom.json')
        self.g = Graph(
            host="127.0.0.1",  # neo4j 搭载服务器的ip地址，ifconfig可获取到
            http_port=7474,  # neo4j 服务器监听的端口号
            user="neo4j",  # 数据库user name，如果没有更改过，应该是neo4j
            password="1234")

    def read_nodes(self):
        # 共3类节点
        drugs = [] # 药品
        diseases = [] #疾病
        symptoms = []#症状

        disease_infos = []#疾病信息
        drug_infos = []  # 疾病信息
        symptom_infos = []  # 疾病信息

        # 构建节点实体关系
        rels_symptom = [] #疾病症状关系
        rels_drug = [] # 疾病药品关系


        count = 0
        for data in open(self.disease_path,encoding='utf-8'):
            disease_dict = {}
            count += 1
            print(count)
            data_json = json.loads(data)
            disease = data_json['name']
            disease_dict['name'] = disease
            diseases.append(disease)
            disease_dict['desc'] = ''
            disease_dict['prevent'] = ''
            disease_dict['cause'] = ''
            disease_dict['treatment'] = ''
            disease_dict['check'] = ''


            if 'symptoms' in data_json:
                if data_json['symptoms']!="":
                    temp=data_json['symptoms']
                    temp=re.split("，|,",temp)
                    symptoms += temp
                    for symptom in temp:
                        rels_symptom.append([disease, symptom])

            if 'drug' in data_json:
                if data_json['drug'] != "":
                    temp = data_json['drug']
                    temp = re.split("，|,",temp)
                    drugs += temp
                    for drug in temp:
                        rels_drug.append([disease, drug])

            if 'desc' in data_json:
                disease_dict['desc'] = data_json['desc']

            if 'prevent' in data_json:
                disease_dict['prevent'] = data_json['prevent']

            if 'cause' in data_json:
                disease_dict['cause'] = data_json['cause']

            if 'check' in data_json:
                disease_dict['check'] = data_json['check']

            if 'treatment' in data_json:
                disease_dict['treatment'] = data_json['treatment']

            disease_infos.append(disease_dict)

        for data in open(self.drug_path, encoding='utf-8'):
            drug_dict = {}
            count += 1
            print(count)
            data_json = json.loads(data)
            drug = data_json['name']
            drug_dict['name'] = drug
            drug_dict['use'] = ''
            drug_dict['adapt'] = ''
            drug_dict['uneffect'] = ''
            drug_dict['forbid'] = ''
            drug_dict['attention'] = ''



            if 'use' in data_json:
                drug_dict['use'] = data_json['use']

            if 'adapt' in data_json:
                drug_dict['adapt'] = data_json['adapt']

            if 'uneffect' in data_json:
                drug_dict['uneffect'] = data_json['uneffect']

            if 'forbid' in data_json:
                drug_dict['forbid'] = data_json['forbid']

            if 'attention' in data_json:
                drug_dict['attention'] = data_json['attention']

            drug_infos.append(drug_dict)

        for data in open(self.symptom_path, encoding='utf-8'):
            symptom_dict = {}
            count += 1
            print(count)
            data_json = json.loads(data)
            symptom = data_json['name']
            symptom_dict['name'] = symptom
            symptom_dict['desc'] = ''

            if 'desc' in data_json:
                symptom_dict['desc'] = data_json['desc']


            symptom_infos.append(symptom_dict)

        return set(drugs),set(symptoms),set(diseases),disease_infos,symptom_infos,drug_infos,rels_symptom,rels_drug

    def export_data(self):
        Drugs, Symptoms, Diseases, disease_infos,symptom_infos,drug_infos, rels_symptom,rels_drug = self.read_nodes()
        print(rels_symptom)
        print(rels_drug)
        f_drug = open('dict/drug.txt', 'w+')
        f_symptom = open('dict/symptoms.txt', 'w+')
        f_disease = open('dict/disease.txt', 'w+')

        f_drug.write('\n'.join(list(Drugs)))
        f_symptom.write('\n'.join(list(Symptoms)))
        f_disease.write('\n'.join(list(Diseases)))

        f_drug.close()
        f_symptom.close()
        f_disease.close()

        return
    def create_file(self):
        ...
        # f_drug = open('dict/drug.txt')
        # for line in f_drug:
        #     f=open("drug/"+str(line.split("\n")[0])+".txt","w+")
        #     f.write("============\n")
        #     f.write("名称\n")
        #     f.write(str(line.split("\n")[0]) + "\n")
        #     f.write("============\n")
        #     f.write("用法用量\n")
        #     f.write("\n")
        #     f.write("============\n")
        #     f.write("适应症\n")
        #     f.write("\n")
        #     f.write("============\n")
        #     f.write("不良反应\n")
        #     f.write("\n")
        #     f.write("============\n")
        #     f.write("禁忌\n")
        #     f.write("\n")
        #     f.write("============\n")
        #     f.write("注意事项\n")
        #     f.write("\n")
        #     f.write("============\n")
        #     f.close()

        # f_symptom = open('dict/symptoms.txt')
        # for line in f_symptom:
        #     f = open("symptom/" + str(line.split("\n")[0]) + ".txt", "w+")
        #     f.write("============\n")
        #     f.write("名称\n")
        #     f.write(str(line.split("\n")[0]) + "\n")
        #     f.write("============\n")
        #     f.write("概述\n")
        #     f.write("\n")
        #     f.write("============\n")
        #     f.close()

    def create_graph(self):
        Drugs, Symptoms, Diseases, disease_infos,symptom_infos,drug_infos, rels_symptom,rels_drug = self.read_nodes()
        count=0
        for disease_dict in disease_infos:
            node = Node("Disease", name=disease_dict['name'], desc=disease_dict['desc'],
                        prevent=disease_dict['prevent'] ,cause=disease_dict['cause'],
                        treatment=disease_dict['treatment'],check=disease_dict['check']
                       )
            self.g.create(node)
            count += 1
            print(count)
        for symptom_dict in symptom_infos:
            node = Node("Symptom", name=symptom_dict['name'], desc=symptom_dict['desc'],
                       )
            self.g.create(node)
            count += 1
            print(count)
        for drug_dict in drug_infos:
            node = Node("Drug", name=drug_dict['name'], use=drug_dict['use'],
                        adapt=drug_dict['adapt'],uneffect=drug_dict['uneffect'],
                        forbid=drug_dict['forbid'],attention=drug_dict['attention']
                       )
            self.g.create(node)
            count += 1
            print(count)
        #建立边
        self.create_relationship('Disease', 'Symptom', rels_symptom, 'has_symptom', '含有症状')
        self.create_relationship('Disease', 'Drug', rels_drug, 'recommend_drug', '宜吃药品')

    def create_relationship(self, start_node, end_node, edges, rel_type, rel_name):
        count = 0
        # 去重处理
        set_edges = []
        for edge in edges:
            set_edges.append('###'.join(edge))
        all = len(set(set_edges))
        for edge in set(set_edges):
            edge = edge.split('###')
            p = edge[0]
            q = edge[1]
            query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                start_node, end_node, p, q, rel_type, rel_name)
            try:
                self.g.run(query)
                count += 1
                print(rel_type, count, all)
            except Exception as e:
                print(e)
        return
if __name__ == '__main__':
    handler = MedicalGraph()
    handler.create_graph()
