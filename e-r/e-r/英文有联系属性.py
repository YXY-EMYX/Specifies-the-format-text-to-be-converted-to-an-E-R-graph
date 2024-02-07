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

        if parts[0] == 'Entity':
            entities.append(parts[1])
        elif parts[0] == 'Attribute':
            attributes.append(parts[1])
        elif parts[0] == 'Relationship':
            current_relationship = {'name': parts[1], 'type1': None, 'type2': None, 'entity1': None, 'entity2': None}
            relationships.append(current_relationship)
        elif parts[0] == 'Type':
            type_parts = parts[1].split(",")
            current_relationship['type1'] = type_parts[0]
            current_relationship['type2'] = type_parts[1]
        elif parts[0] == 'Connect':
            entity1, relationship, entity2 = parts[1].split()
            current_relationship['entity1'] = entity1
            current_relationship['entity2'] = entity2

    return {'entities': entities, 'attributes': attributes, 'relationships': relationships}


def create_er_diagram(parsed_data: Dict[str, List]):
    er_diagram = Digraph('ER', filename='er_diagram.gv', format='png')
    er_diagram.attr(rankdir='TB', size='10,16')

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
Entity: Customer
Attribute: Customer.CustomerID
Attribute: Customer.ContactName
Attribute: Customer.City

Entity: Order
Attribute: Order.OrderID
Attribute: Order.OrderDate
Attribute: Order.ShipCity

Relationship: Places
Type: 1,n
Connect: Customer Places Order

Relationship: Contains
Type: 1,n
Connect: Order Contains Product

Attribute: Places.Date
Attribute: Places.Amount
Attribute: Contains.Quantity
Attribute: Contains.Price
"""

parsed_data = parse_input_text(input_text)
create_er_diagram(parsed_data)
