import yaml
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# YAMLデータを読み込む
yaml_data = """
topomap:
  - node:
      id: 1
      edge: 
        - id: 1
          deg: -90
      type: dead_end
  - node:
      id: 2
      edge:
        - id: 2
          deg: 0
        - id: 1
          deg: 90
      type: corner
  - node:
      id: 3
      edge:
        - id: 2
          deg: 180
        - id: 3
          deg: -90
      type: corner
  - node:
      id: 4
      edge: 
        - id: 3
          deg: 90
      type: dead_end
  - edge:
      id: 1
  - edge:
      id: 2
  - edge:
      id: 3
"""

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

# ノードとエッジをグラフに追加し、位置とエッジIDを計算
edge_labels = {}  # エッジのラベルを格納する辞書
for item in data['topomap']:
    if 'node' in item:
        node_data = item['node']
        node_id = node_data['id']
        node_type = node_data['type']
        G.add_node(node_id,type=node_type)
        print(pos)
        for edge_info in node_data['edge']:
            edge_id = edge_info['id']
            deg = edge_info['deg']
            rad = np.radians(deg)  # 角度をラジアンに変換
            # print(edge_id)
            # 隣接ノードのIDを探す
            for other_item in data['topomap']:
                if 'node' in other_item and other_item['node']['id'] != node_id:
                    other_node_data = other_item['node']
                    if any(edge['id'] == edge_id for edge in other_node_data['edge']):
                        other_node_id = other_node_data['id']
                        if other_node_id not in pos:
                            # 隣接ノードの位置を計算
                            pos[other_node_id] = (
                                pos[node_id][0] + edge_length * np.cos(rad),
                                pos[node_id][1] + edge_length * np.sin(rad)
                            )
                        # エッジを追加し、エッジIDを属性として設定
                        G.add_edge(node_id, other_node_id, id=edge_id)
                        # エッジラベルの設定
                        edge_labels[(node_id, other_node_id)] = str(edge_id)
node_colors = [type_color_dict[G.nodes[node]["type"]] for node in G.nodes()]
# グラフを描画
nx.draw(G, pos, with_labels=True, node_size=800, edge_color='gray', node_color=node_colors, font_size=12)
# エッジラベルを描画
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

plt.show()
