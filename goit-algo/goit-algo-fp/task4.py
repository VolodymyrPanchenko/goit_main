import uuid
import networkx as nx
import matplotlib.pyplot as plt

class Node:
    def __init__(self, key, color="skyblue"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())

def add_edges(graph, node, pos, x=0, y=0, layer=1):
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val)
        if node.left:
            graph.add_edge(node.id, node.left.id)
            l = x - 1 / 2 ** layer
            pos[node.left.id] = (l, y - 1)
            add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)
        if node.right:
            graph.add_edge(node.id, node.right.id)
            r = x + 1 / 2 ** layer
            pos[node.right.id] = (r, y - 1)
            add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)
    return graph

def draw_tree(tree_root, figsize=(8, 5)):
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    add_edges(tree, tree_root, pos)

    colors = [data['color'] for _, data in tree.nodes(data=True)]
    labels = {n_id: data['label'] for n_id, data in tree.nodes(data=True)}

    plt.figure(figsize=figsize)
    nx.draw(tree, pos=pos, labels=labels, arrows=False, 
            node_size=2500, node_color=colors)
    plt.axis('off')
    plt.show()

# ----------- проста функція для побудови дерева з масиву -----------

def array_to_tree(arr):
    """
    Перетворює масив arr у повне бінарне дерево.
    """
    if not arr:
        return None

    nodes = [Node(val) for val in arr]

    for i in range(len(arr)):
        li, ri = 2 * i + 1, 2 * i + 2
        if li < len(arr):
            nodes[i].left = nodes[li]
        if ri < len(arr):
            nodes[i].right = nodes[ri]

    return nodes[0]  # корінь дерева

# ---------------- Приклад використання ----------------

heap_array = [10, 4, 15, 2, 8, 20, 25]

root = array_to_tree(heap_array)
draw_tree(root)
