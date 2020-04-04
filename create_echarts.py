#-*-coding:utf-8-*-
from py2neo import Graph
from pyecharts import options as opts
from pyecharts.charts import Graph as gr
from tool.jscode import JsCode


class CreateEcharts:
    def __init__(self):
        self.g = Graph(
            host="127.0.0.1",
            http_port=7474,
            user="neo4j",
            password="1234")
        self.num_limit = 50

    #疾病的关系图
    def create_disease(self,keyname,url):
        entities=[]
        entities.append(keyname)
        sqls=[]
        #疾病的介绍
        sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.desc".format(i) for i in entities]
        sqls.append(sql)

        #疾病的病因
        sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.cause".format(i) for i in entities]
        sqls.append(sql)

        #疾病的治疗
        sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.treatment".format(i) for i in entities]
        sqls.append(sql)

        #疾病的预防
        sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.prevent".format(i) for i in entities]
        sqls.append(sql)

        #疾病的检查
        sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.check".format(i) for i in entities]
        sqls.append(sql)

        # 疾病的药品
        sql = ["MATCH (m:Disease)-[r:recommend_drug]->(n:Drug) where m.name = '{0}' return m.name, r.name, n.name".format(i)
               for i in entities]
        sqls.append(sql)

        #疾病的症状
        sql = ["MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where m.name = '{0}' return m.name, r.name, n.name".format(i) for
           i in entities]
        sqls.append(sql)

        answers=[]
        for s in sqls:

            ress = self.g.run(s[0]).data()
            #print(ress)
            if len(ress)==0 or '' in ress[0].values():#没查到
                continue
            for r in ress:
                print(r)
                if(len(list(r.keys()))==2):#代表前五项
                    answers.append([list(r.keys())[1].split('.')[1],r[list(r.keys())[1]]])
                else:#代表药品和症状
                    if r['r.name']=="宜吃药品":
                        answers.append(["recommend_drug",r['n.name']])
                    else:
                        answers.append(["has_symptom", r['n.name']])
        #answers结果list
        for i in range(len(answers)):
            print(answers[i])

        #统计category类别
        types = set()
        types.add("disease")
        relation_types = set()
        for i in range(len(answers)):
            relation_types.add(answers[i][0])
        for i in range(len(answers)):
            if '_' in answers[i][0]:
                types.add(answers[i][0].split('_')[1])
            else:
                types.add(answers[i][0])
        categories = []  # 存储与center_name有关系的数据的类型
        categories.append({})
        for x in types:
            categories.append({'name': x})
        print(categories)



        #创建nodes
        nodes=[]
        nodes.append({"name": entities[0]+"|disease" , "des": entities[0],
                      "category": categories.index({'name': "disease"}), "symbolSize": 90})
        for x in relation_types:
            nodes.append({"name": x + "|centernode", "des": "", "symbolSize": 30})

        for i in range(len(answers)):
            if "_" in answers[i][0]:
                cate=answers[i][0].split("_")[1]
            else:
                cate=answers[i][0]
            node = {"name": answers[i][1]+"|"+cate ,
                    "des": answers[i][1],
                    "category": categories.index({'name': cate}), "symbolSize": 70}
            if node not in nodes:
                nodes.append(node)
        for n in nodes:
            print(n)  # nodes创建完成

        #创建关系
        links=[]
        for x in relation_types:

            links.append({"source": entities[0]+"|disease", "target": x+"|centernode",
                      "name": x})

        for i in range(len(answers)):
            if "_" in answers[i][0]:
                cate=answers[i][0].split("_")[1]
            else:
                cate=answers[i][0]
            links.append({"source": answers[i][0]+"|centernode", "target": answers[i][1]+"|"+cate,
                      "name": " "})

        #建图
        c = (
            gr(init_opts=opts.InitOpts(width="100%", height="700px"))
                .add("", nodes, links, categories=categories,
                     repulsion=2500, label_opts=opts.LabelOpts(position="inside", formatter=JsCode(
                    """function (x) { var strs = x.data.name;   var n='';    var str='centernode';   if(strs.search(str)!=-1) {return  n;}   var strs = x.data.name.split('|')[0];  if(strs.length<=6){                       return strs;                   }else {                       name = strs.slice(0,6) + '...';                        return name;                   }}""").js_code),
                     tooltip_opts=opts.TooltipOpts(formatter=JsCode(
                         """function (x) { if(x.dataType === 'edge'){return x.data.name;} var strs = x.data.des;  var str = ''; for(var i = 0, s; s = strs[i++];) { if(i==500){str+='...'; break;} str += s; if(!(i % 50)) str += '<br>'; } return str;}""").js_code),
                     edge_label=opts.LabelOpts(position="",
                                               formatter=JsCode("""function (x) {return x.data.name;}""").js_code),
                     edge_symbol=['circle', 'arrow'], edge_symbol_size=[4, 10], is_focusnode="true"
                     )
                .set_global_opts(title_opts=opts.TitleOpts(title=entities[0] + "相关知识图谱"))

        )
        c.render(url)

    def create_symptom(self,keyname,url):
        entities = []
        entities.append(keyname)
        sqls = []

        #症状概述
        sql = ["MATCH (m:Symptom) where m.name = '{0}' return m.name, m.desc".format(i) for i in entities]
        sqls.append(sql)

        #症状疾病
        sql = ["MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
        sqls.append(sql)

        answers = []
        for s in sqls:

            ress = self.g.run(s[0]).data()
            #print(ress)
            for r in ress:
                if (len(list(r.keys())) == 2):  # 代表前五项
                    answers.append([list(r.keys())[1].split('.')[1], r[list(r.keys())[1]]])
                else:  # 代表药品和症状
                    answers.append(["accompany_disease", r['m.name']])
        for i in range(len(answers)):
            print(answers[i])

        # 统计category类别
        types = set()#代表节点类别
        types.add("symptom")
        relation_types = set()#代表边的类别
        for i in range(len(answers)):
            relation_types.add(answers[i][0])
        for i in range(len(answers)):
            if '_' in answers[i][0]:
                types.add(answers[i][0].split('_')[1])
            else:
                types.add(answers[i][0])
        categories = []  # 存储与center_name有关系的数据的类型
        categories.append({})
        for x in types:
            categories.append({'name': x})
        print(categories)

        # 创建nodes
        nodes = []
        nodes.append({"name": entities[0]+"|symptom", "des": entities[0],
                      "category": categories.index({'name': "symptom"}), "symbolSize": 90})
        for x in relation_types:
            nodes.append({"name": x + "|centernode", "des": "", "symbolSize": 30})

        for i in range(len(answers)):
            if "_" in answers[i][0]:
                cate = answers[i][0].split("_")[1]
            else:
                cate = answers[i][0]
            node = {"name": answers[i][1]+"|"+cate,
                    "des": answers[i][1],
                    "category": categories.index({'name': cate}), "symbolSize": 70}
            if node not in nodes:
                nodes.append(node)
        for n in nodes:
            print(n)  # nodes创建完成

        # 创建关系
        links = []
        for x in relation_types:
            links.append({"source": entities[0]+"|symptom", "target": x + "|centernode",
                          "name": x})

        for i in range(len(answers)):
            if "_" in answers[i][0]:
                cate = answers[i][0].split("_")[1]
            else:
                cate = answers[i][0]
            links.append({"source": answers[i][0] + "|centernode", "target": answers[i][1]+"|"+cate,
                          "name": " "})

        # 建图
        c = (
            gr(init_opts=opts.InitOpts(width="100%", height="700px"))
                .add("", nodes, links, categories=categories,
                     repulsion=2500, label_opts=opts.LabelOpts(position="inside", formatter=JsCode(
                    """function (x) { var strs = x.data.name;   var n='';    var str='centernode';   if(strs.search(str)!=-1) {return  n;}   var strs = x.data.name.split('|')[0];  if(strs.length<=6){                       return strs;                   }else {                       name = strs.slice(0,6) + '...';                        return name;                   }}""").js_code),
                     tooltip_opts=opts.TooltipOpts(formatter=JsCode(
                         """function (x) { if(x.dataType === 'edge'){return x.data.name;} var strs = x.data.des;  var str = ''; for(var i = 0, s; s = strs[i++];) { if(i==500){str+='...'; break;} str += s; if(!(i % 50)) str += '<br>'; } return str;}""").js_code),
                     edge_label=opts.LabelOpts(position="",
                                               formatter=JsCode("""function (x) {return x.data.name;}""").js_code),
                     edge_symbol=['circle', 'arrow'], edge_symbol_size=[4, 10], is_focusnode="true"
                     )
                .set_global_opts(title_opts=opts.TitleOpts(title=entities[0] + "相关知识图谱"))

        )
        c.render(url)

    def create_drug(self,keyname,url):
        entities = []
        entities.append(keyname)
        sqls = []

        #药品使用说明
        sql = ["MATCH (m:Drug) where m.name = '{0}' return m.name, m.use".format(i) for i in entities]
        sqls.append(sql)

        #药品的不良反应
        sql = ["MATCH (m:Drug) where m.name = '{0}' return m.name, m.uneffect".format(i) for i in entities]
        sqls.append(sql)

        #药品禁忌
        sql = ["MATCH (m:Drug) where m.name = '{0}' return m.name, m.forbid".format(i) for i in entities]
        sqls.append(sql)

        #药品注意事项
        sql = ["MATCH (m:Drug) where m.name = '{0}' return m.name, m.attention".format(i) for i in entities]
        sqls.append(sql)

        #药品对应的疾病
        sql = ["MATCH (m:Disease)-[r:recommend_drug]->(n:Drug) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
        sqls.append(sql)

        answers = []
        for s in sqls:

            ress = self.g.run(s[0]).data()
            #print(ress)
            for r in ress:
                if (len(list(r.keys())) == 2):  # 代表前五项
                    answers.append([list(r.keys())[1].split('.')[1], r[list(r.keys())[1]]])
                else:  # 代表药品和症状
                    answers.append(["cure_disease", r['m.name']])
        for i in range(len(answers)):
            print(answers[i])

        # 统计category类别
        types = set()  # 代表节点类别
        types.add("drug")
        relation_types = set()  # 代表边的类别
        for i in range(len(answers)):
            relation_types.add(answers[i][0])
        for i in range(len(answers)):
            if '_' in answers[i][0]:
                types.add(answers[i][0].split('_')[1])
            else:
                types.add(answers[i][0])
        categories = []  # 存储与center_name有关系的数据的类型
        categories.append({})
        for x in types:
            categories.append({'name': x})
        print(categories)

        # 创建nodes
        nodes = []
        nodes.append({"name": entities[0]+"|drug", "des": entities[0],
                      "category": categories.index({'name': "drug"}), "symbolSize": 90})
        for x in relation_types:
            nodes.append({"name": x + "|centernode", "des": "", "symbolSize": 20})

        for i in range(len(answers)):
            if "_" in answers[i][0]:
                cate = answers[i][0].split("_")[1]
            else:
                cate = answers[i][0]
            node = {"name": answers[i][1]+"|"+cate,
                    "des": answers[i][1],
                    "category": categories.index({'name': cate}), "symbolSize": 70}
            if node not in nodes:
                nodes.append(node)
        for n in nodes:
            print(n)  # nodes创建完成

        # 创建关系
        links = []
        for x in relation_types:
            links.append({"source": entities[0]+"|drug", "target": x + "|centernode",
                          "name": x})

        for i in range(len(answers)):
            if "_" in answers[i][0]:
                cate = answers[i][0].split("_")[1]
            else:
                cate = answers[i][0]
            links.append({"source": answers[i][0] + "|centernode", "target": answers[i][1]+"|"+cate,
                          "name": " "})

        # 建图
        c = (
            gr(init_opts=opts.InitOpts(width="100%", height="700px"))
                .add("", nodes, links, categories=categories,
                     repulsion=2500, label_opts=opts.LabelOpts(position="inside", formatter=JsCode(
                    """function (x) { var strs = x.data.name;   var n='';    var str='centernode';   if(strs.search(str)!=-1) {return  n;}   var strs = x.data.name.split('|')[0];  if(strs.length<=6){                       return strs;                   }else {                       name = strs.slice(0,6) + '...';                        return name;                   }}""").js_code),
                     tooltip_opts=opts.TooltipOpts(formatter=JsCode(
                         """function (x) { if(x.dataType === 'edge'){return x.data.name;} var strs = x.data.des;  var str = ''; for(var i = 0, s; s = strs[i++];) { if(i==500){str+='...'; break;} str += s; if(!(i % 50)) str += '<br>'; } return str;}""").js_code),
                     edge_label=opts.LabelOpts(position="",
                                               formatter=JsCode("""function (x) {return x.data.name;}""").js_code),
                     edge_symbol=['circle', 'arrow'], edge_symbol_size=[4, 10], is_focusnode="true"
                     )
                .set_global_opts(title_opts=opts.TitleOpts(title=entities[0] + "相关知识图谱"))

        )
        c.render(url)


if __name__ == '__main__':
    searcher = CreateEcharts()
    searcher.create_disease("双相情感障碍","templates//echarts//render1"+".html")