
class QuestionPaser:

    '''构建实体节点'''
    def build_entitydict(self, args):
        entity_dict = {}
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)

        return entity_dict

    '''解析主函数'''
    def parser_main(self, res_classify):
        args = res_classify['args']
        entity_dict = self.build_entitydict(args)
        question_types = res_classify['question_types']
        sqls = []
        for question_type in question_types:
            sql_ = {}
            sql_['question_type'] = question_type
            sql = []
            if question_type == 'disease_symptom':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'symptom_disease':
                sql = self.sql_transfer(question_type, entity_dict.get('symptom'))

            elif question_type == 'disease_cause':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_drug':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'drug_disease':
                sql = self.sql_transfer(question_type, entity_dict.get('drug'))

            elif question_type == 'disease_check':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_prevent':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_treatment':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'drug_use':
                sql = self.sql_transfer(question_type, entity_dict.get('drug'))

            elif question_type == 'drug_uneffect':
                sql = self.sql_transfer(question_type, entity_dict.get('drug'))

            elif question_type == 'drug_forbid':
                sql = self.sql_transfer(question_type, entity_dict.get('drug'))

            elif question_type == 'drug_attention':
                sql = self.sql_transfer(question_type, entity_dict.get('drug'))


            elif question_type == 'disease_desc':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'symptom_desc':
                sql = self.sql_transfer(question_type, entity_dict.get('symptom'))

            if sql:
                sql_['sql'] = sql

                sqls.append(sql_)

        return sqls

    '''针对不同的问题，分开进行处理'''
    def sql_transfer(self, question_type, entities):
        if not entities:
            return []

        # 查询语句
        sql = []
        # 查询疾病的原因
        if question_type == 'disease_cause':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.cause".format(i) for i in entities]

        # 查询疾病的防御措施
        elif question_type == 'disease_prevent':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.prevent".format(i) for i in entities]


        # 查询疾病的治疗方式
        elif question_type == 'disease_treatment':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.treatment".format(i) for i in entities]

        # 查询疾病的相关介绍
        elif question_type == 'disease_desc':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.desc".format(i) for i in entities]

        #查询症状的介绍
        elif question_type == 'symptom_desc':
            sql = ["MATCH (m:Symptom) where m.name = '{0}' return m.name, m.desc".format(i) for i in entities]

        # 查询疾病有哪些症状
        elif question_type == 'disease_symptom':
            sql = ["MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        # 查询症状会导致哪些疾病
        elif question_type == 'symptom_disease':
            sql = ["MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        # 查询疾病常用药品
        elif question_type == 'disease_drug':
            sql = ["MATCH (m:Disease)-[r:recommend_drug]->(n:Drug) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]


        # 已知药品查询能够治疗的疾病
        elif question_type == 'drug_disease':
            sql = ["MATCH (m:Disease)-[r:recommend_drug]->(n:Drug) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        # 查询疾病应该进行的检查
        elif question_type == 'disease_check':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.check".format(i) for i in entities]

        # 查询药品的使用说明
        elif question_type == 'drug_use':
            sql = ["MATCH (m:Drug) where m.name = '{0}' return m.name, m.use".format(i) for i in entities]

        # 查询药品的不良反应
        elif question_type == 'drug_uneffect':
            sql = ["MATCH (m:Drug) where m.name = '{0}' return m.name, m.uneffect".format(i) for i in entities]

        # 查询药品的禁忌
        elif question_type == 'drug_forbid':
            sql = ["MATCH (m:Drug) where m.name = '{0}' return m.name, m.forbid".format(i) for i in entities]

        # 查询药品的注意事项
        elif question_type == 'drug_attention':
            sql = ["MATCH (m:Drug) where m.name = '{0}' return m.name, m.attention".format(i) for i in entities]


        return sql



if __name__ == '__main__':
    handler = QuestionPaser()
