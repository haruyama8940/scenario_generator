import yaml
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# YAMLデータを読み込む
yaml_file_path = '/home/rdclab/orne_ws/src/scenario_generator/config/topo_cit3f.yaml'
with open(yaml_file_path) as yaml_data:
    data = yaml.load(yaml_data, Loader=yaml.FullLoader)

type_color_dict = {"straight_road":"blue", "dead_end":"lime", "corner":"green","3way":"red"}
                #    , "corner", "cross_road", "3way_right", "3way_center", "3way_left"]
# color_list = ["blue", "lime", "blueviolet", "green", "gold", "aqua", "red", "orange"]

# グラフを作成
G = nx.Graph()
pos = {}  # ノードの位置を格納する辞書
edge_length = 1  # すべてのエッジの長さを一定とする

# 初期ノードの位置を設定
pos[1] = (0, 0)  # 最初のノードの位置を原点とする

# Register all nodes
edge_labels = {}
edge_to_nodes = {}
edge_info_dict = {} 

for item in data['topomap']:
    if 'node' in item:
        node_data = item['node']
        node_id = node_data['id']
        node_type = node_data['type']
        G.add_node(node_id,type=node_type)
        # print(node_data)
        # print(pos)
        #Register edge data for current node
        for edge_info in node_data['edge']:
            edge_id = edge_info['id']
            deg = edge_info['deg']
            edge_info_dict[(node_id,edge_id)] = deg #Registar deg using node_id and edge_id as keys
            if edge_id not in edge_to_nodes :
                edge_to_nodes[edge_id] =[]
            edge_to_nodes[edge_id].append(node_id)
            # print(edge_info_dict)
#Register edge 
for edge_id, nodes in edge_to_nodes.items():
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            edge_in_node_id1 = nodes[i]
            edge_in_node_id2 = nodes[j]
    # for edge_id1, edge_id2  in edge_to_nodes[edge_id]:
            # print(edge_in_node_id1,edge_in_node_id2)
            G.add_edge(edge_in_node_id1,edge_in_node_id2,id=edge_id)



# pos[1] = (0.0)
pos = {1: (0,0)} # The position of the initial node is the origin.

for (node_id,edge_id),deg in  edge_info_dict.items():
    # print(pos)
    if node_id in pos: #nodeの位置を現在のnodeをもとに決定
        rad = np.radians(deg)  # 角度をラジアンに変換
        for other_node_id in edge_to_nodes[edge_id]:
            if node_id != other_node_id and other_node_id not in pos:
                pos[other_node_id] = (
                                    pos[node_id][0] + edge_length * np.cos(rad),
                                    pos[node_id][1] + edge_length * np.sin(rad)
                                    )
pos2 = dict(sorted(pos.items()))
print(pos)
print(pos2)
# for node_id,(pos_x,pos_y) in pos.items():
#     print(node_id)

#     for edge_info in data['topomap']:
#         if 'node' in other_item and other_item['node']['id'] != node_id:
#             other_node_data = other_item['node']
#             if other_node_id not in pos:


#     for other_item in G.nodes:
#         if other_node_id != node_id and G.has_edge(node_id,other_node_id):
#                 if 'node' in other_item and other_item['node']['id'] != node_id:
#                     other_node_data = other_item['node']
#                     if any(edge['id'] == edge_id for edge in other_node_data['edge']):
#                         other_node_id = other_node_data['id']
#                         if other_node_id not in pos:
#                             # 隣接ノードの位置を計算
#                             pos[other_node_id] = (
#                                 pos[node_id][0] + edge_length * np.cos(rad),
#                                 pos[node_id][1] + edge_length * np.sin(rad)
#                             )
# #                         # エッジを追加し、エッジIDを属性として設定
# #                         G.add_edge(node_id, other_node_id, id=edge_id)
# #                         # エッジラベルの設定
# #                         edge_labels[(node_id, other_node_id)] = str(edge_id)
node_colors = [type_color_dict[G.nodes[node]["type"]] for node in G.nodes()]
# # # グラフを描画
# nx.draw(G, pos, with_labels=True, node_size=800, edge_color='gray', node_color=node_colors, font_size=12)
nx.draw(G, pos2,with_labels=True, node_size=800, node_color=node_colors,edge_color='gray', font_size=12)
# # # エッジラベルを描画
# nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

plt.show()
