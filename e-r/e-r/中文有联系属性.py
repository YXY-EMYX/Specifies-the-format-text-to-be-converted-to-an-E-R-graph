
from graphviz import Digraph
from typing import List, Dict

def parse_input_text(input_text: str) -> Dict[str, List]:
    lines = input_text.strip().split('\n')

    entities = []
    attributes = []
    relationships = []

    current_relationship = None

    for line in lines:
        parts = line.split(': ')

        if parts[0] == '实体':
            entities.append(parts[1])
        elif parts[0] == '属性':
            attributes.append(parts[1])
        elif parts[0] == '关系':
            current_relationship = {'name': parts[1], 'type1': None, 'type2': None, 'entity1': None, 'entity2': None}
            relationships.append(current_relationship)
        elif parts[0] == '类型':
            type_parts = parts[1].split(",")
            current_relationship['type1'] = type_parts[0]
            current_relationship['type2'] = type_parts[1]
        elif parts[0] == '连接':
            entity1, relationship, entity2 = parts[1].split()
            current_relationship['entity1'] = entity1
            current_relationship['entity2'] = entity2

    return {'entities': entities, 'attributes': attributes, 'relationships': relationships}

def create_er_diagram(parsed_data: Dict[str, List]):
    er_diagram = Digraph('ER', filename='er_diagram.gv', format='png')
    er_diagram.attr(rankdir='TB', size='20,16')

    # 指定字体为微软雅黑
    er_diagram.attr('graph', fontname='Microsoft YaHei')
    er_diagram.attr('node', fontname='Microsoft YaHei')
    er_diagram.attr('edge', fontname='Microsoft YaHei')

    # 添加实体
    for entity in parsed_data['entities']:
        er_diagram.node(entity, shape='rectangle')

    # 添加关系和关系类型
    for relationship in parsed_data['relationships']:
        er_diagram.node(relationship['name'], shape='diamond')
        er_diagram.edge(relationship['entity1'], relationship['name'], label=relationship['type1'], dir='none')
        er_diagram.edge(relationship['name'], relationship['entity2'], label=relationship['type2'], dir='none')

    # 添加属性
    for attribute in parsed_data['attributes']:
        attribute_parts = attribute.split('.')
        er_diagram.node(attribute, shape='ellipse')
        er_diagram.edge(attribute_parts[0], attribute, dir='none')

    # 生成 E-R 图
    er_diagram.render()


input_text = """
实体: 车间
属性: 车间.车间编号
属性: 车间.车间主任姓名
属性: 车间.地址
属性: 车间.电话

实体: 工人
属性: 工人.职工号
属性: 工人.姓名
属性: 工人.年龄
属性: 工人.性别
属性: 工人.工种
属性: 工人.车间编号

实体: 产品
属性: 产品.产品编号
属性: 产品.价格

实体: 零件
属性: 零件.零件编号
属性: 零件.重量
属性: 零件.价格

关系: 产品_零件
类型: n,m
连接: 产品 产品_零件 零件

关系: 车间_工人
类型: 1,n
连接: 车间 车间_工人 工人

关系: 车间_产品
类型: 1,n
连接: 车间 车间_产品 产品

关系: 车间_零件
类型: n,m
连接: 车间 车间_零件 零件

实体: 仓库
属性: 仓库.仓库编号
属性: 仓库.仓库主任姓名
属性: 仓库.电话

关系: 产品_仓库
类型: n,m
连接: 产品 产品_仓库 仓库

关系: 零件_仓库
类型: n,m
连接: 零件 零件_仓库 仓库
"""


parsed_data = parse_input_text(input_text)
create_er_diagram(parsed_data)
