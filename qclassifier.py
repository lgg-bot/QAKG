import os
import ahocorasick

class QuestionClassifier:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])#os.path.abspath(__file__)返回当前脚本的绝对路径
        #　特征词路径
        self.disease_path = os.path.join(cur_dir, 'dict/disease.txt')
        self.drug_path = os.path.join(cur_dir, 'dict/drug.txt')
        self.symptom_path = os.path.join(cur_dir, 'dict/symptoms.txt')
        # 加载特征词
        self.disease_wds= [i.strip() for i in open(self.disease_path) if i.strip()]
        self.drug_wds= [i.strip() for i in open(self.drug_path) if i.strip()]
        self.symptom_wds= [i.strip() for i in open(self.symptom_path) if i.strip()]
        self.region_words = set(self.disease_wds + self.drug_wds  +  self.symptom_wds)
        # 构造领域actree
        self.region_tree = self.build_actree(list(self.region_words))#只是对医疗的实体构建actree，不对下面的口语建
        # 构建词典
        self.wdtype_dict = self.build_wdtype_dict()
        # 问句疑问词
        self.symptom_words = ['症状', '表征', '现象', '症候', '表现']
        self.cause_words = ['原因','病因','成因', '为什么', '怎么会', '怎样才', '咋样才', '怎样会', '如何会', '为啥', '为何', '如何才会', '怎么才会', '会导致', '会造成']
        self.drug_words = ['药', '药品', '用药', '胶囊', '口服液', '炎片']
        self.prevent_words = ['预防', '防范', '抵制', '抵御', '避免','防止','躲避','逃避','避开','免得','逃开','避开','避掉','躲开','躲掉','绕开','怎样才能不', '怎么才能不', '咋样才能不','咋才能不', '如何才能不','怎样才不', '怎么才不', '咋样才不','咋才不', '如何才不','怎样才可以不', '怎么才可以不', '咋样才可以不', '咋才可以不', '如何可以不','怎样才可不', '怎么才可不', '咋样才可不', '咋才可不', '如何可不']
        self.check_word = ['检查', '检查项目', '查出', '检查', '测出', '试出']
        self.treatment_words = ['治疗', '治什么','治疗什么', '治啥', '治疗啥', '医治啥', '治愈啥', '主治啥', '主治什么', '有什么用', '有何用', '用处', '用途','有什么好处', '有什么益处', '有何益处', '用来', '用来做啥', '用来作甚', ]
        self.use_words=['怎么吃', '怎样吃', '怎么用', '怎么服用', '用法', '用量', '吃多少']
        self.uneffect_words=['不良反应', '副作用']
        self.forbid_words=['不能吃', '不宜吃', '不应该吃', '禁忌','能不能吃']
        self.attention_words=['注意', '注意事项']
        print('model init finished ......')

        return

    '''分类主函数'''
    def classify(self, question):
        data = {}
        medical_dict = self.check_medical(question)
        if not medical_dict:
            return {}
        data['args'] = medical_dict
        #收集问句当中所涉及到的实体类型
        types = []
        for type_ in medical_dict.values():
            types += type_

        question_types = []

        # 症状
        if self.check_words(self.symptom_words, question) and ('disease' in types):
            question_type = 'disease_symptom'
            question_types.append(question_type)

        if self.check_words(self.symptom_words, question) and ('symptom' in types):#我总是头晕，一般什么病会有这种症状呢
            question_type = 'symptom_disease'
            question_types.append(question_type)

        # 原因
        if self.check_words(self.cause_words, question) and ('disease' in types):
            question_type = 'disease_cause'
            question_types.append(question_type)


        # 推荐药品
        if self.check_words(self.drug_words, question) and 'disease' in types:
            question_type = 'disease_drug'
            question_types.append(question_type)

        # 药品治啥病
        if self.check_words(self.treatment_words, question) and 'drug' in types:
            question_type = 'drug_disease'
            question_types.append(question_type)

        # 疾病接受检查项目
        if self.check_words(self.check_word, question) and 'disease' in types:
            question_type = 'disease_check'
            question_types.append(question_type)

        #　疾病防御
        if self.check_words(self.prevent_words, question) and 'disease' in types:
            question_type = 'disease_prevent'
            question_types.append(question_type)

        # 疾病治疗方式
        if self.check_words(self.treatment_words, question) and 'disease' in types:
            question_type = 'disease_treatment'
            question_types.append(question_type)

        #药品用法
        if self.check_words(self.use_words, question) and 'drug' in types:
            question_type = 'drug_use'
            question_types.append(question_type)

        #药品不良反应
        if self.check_words(self.uneffect_words, question) and 'drug' in types:
            question_type = 'drug_uneffect'
            question_types.append(question_type)

        #药品禁忌
        if self.check_words(self.forbid_words, question) and 'drug' in types:
            question_type = 'drug_forbid'
            question_types.append(question_type)

        #药品注意事项
        if self.check_words(self.attention_words, question) and 'drug' in types:
            question_type = 'drug_attention'
            question_types.append(question_type)



        # 若没有查到相关的外部查询信息，那么则将该疾病的描述信息返回
        if question_types == [] and 'disease' in types:
            question_types = ['disease_desc']

        # 若没有查到相关的外部查询信息，那么则将该疾病的描述信息返回
        if question_types == [] and 'symptom' in types:
            question_types = ['symptom_desc']

        # 将多个分类结果进行合并处理，组装成一个字典
        data['question_types'] = question_types
        print(question_types)
        return data

    '''构造词对应的类型'''
    def build_wdtype_dict(self):
        wd_dict = dict()
        for wd in self.region_words:
            wd_dict[wd] = []
            if wd in self.disease_wds:
                wd_dict[wd].append('disease')
            if wd in self.drug_wds:
                wd_dict[wd].append('drug')
            if wd in self.symptom_wds:
                wd_dict[wd].append('symptom')

        return wd_dict

    '''构造actree，加速过滤'''
    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    '''问句过滤'''
    def check_medical(self, question):
        region_wds = []
        for i in self.region_tree.iter(question):
            wd = i[1][1]
            region_wds.append(wd)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        final_wds = [i for i in region_wds if i not in stop_wds]
        final_dict = {i:self.wdtype_dict.get(i) for i in final_wds}

        return final_dict

    '''基于特征词进行分类'''
    def check_words(self, wds, sent):
        for wd in wds:
            if wd in sent:
                return True
        return False


if __name__ == '__main__':
    handler = QuestionClassifier()
    while 1:
        question = input('input an question:')
        data = handler.classify(question)
        print(data)