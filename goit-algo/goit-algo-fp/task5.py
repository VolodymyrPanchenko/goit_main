import uuid
import networkx as nx
import matplotlib.pyplot as plt


# -------------------- Клас вузла --------------------

class Node:
    def __init__(self, key, color="skyblue"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())


# -------------------- Малювання дерева --------------------

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


def draw_tree(tree_root, title="Дерево"):
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    add_edges(tree, tree_root, pos)

    colors = [data['color'] for _, data in tree.nodes(data=True)]
    labels = {n_id: data['label'] for n_id, data in tree.nodes(data=True)}

    plt.figure(figsize=(10, 6))
    nx.draw(tree, pos=pos, labels=labels, arrows=False,
            node_size=2500, node_color=colors, font_size=14, font_weight='bold')
    plt.title(title, fontsize=16, pad=20)
    plt.axis('off')
    plt.tight_layout()
    plt.show()


# -------------------- Генерація градієнта кольорів --------------------

def generate_colors(n):
    """Генерує n кольорів від темного до світлого у форматі #RRGGBB"""
    colors = []
    for i in range(n):
        # Від темного (#1A1A2E) до світлого (#E8F4F8)
        # Інтерполяція для R, G, B каналів
        ratio = i / (n - 1) if n > 1 else 0
        
        r = int(26 + (232 - 26) * ratio)    # 26 -> 232
        g = int(26 + (244 - 26) * ratio)    # 26 -> 244
        b = int(46 + (248 - 46) * ratio)    # 46 -> 248
        
        colors.append(f'#{r:02X}{g:02X}{b:02X}')
    
    return colors


# -------------------- Обхід У ШИРИНУ (BFS) - використовує ЧЕРГУ --------------------

def bfs_traversal(root):
    """Обхід у ширину з використанням черги"""
    if not root:
        return []
    
    visited = []
    queue = [root]  # Черга: додаємо в кінець, беремо з початку
    
    while queue:
        node = queue.pop(0)  # Беремо перший елемент (FIFO - First In First Out)
        visited.append(node)
        
        # Додаємо дітей у чергу
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    
    return visited


# -------------------- Обхід У ГЛИБИНУ (DFS) - використовує СТЕК --------------------

def dfs_traversal(root):
    """Обхід у глибину з використанням стека"""
    if not root:
        return []
    
    visited = []
    stack = [root]  # Стек: додаємо в кінець, беремо з кінця
    
    while stack:
        node = stack.pop()  # Беремо останній елемент (LIFO - Last In First Out)
        visited.append(node)
        
        # Додаємо дітей у стек (ВАЖЛИВО: спочатку правого, потім лівого!)
        # Так лівий буде оброблений першим
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    
    return visited


# -------------------- Візуалізація обходу --------------------

def visualize_traversal(root, traversal_type='bfs'):
    """
    Візуалізує обхід дерева
    
    traversal_type: 'bfs' для обходу в ширину, 'dfs' для обходу в глибину
    """
    # Виконуємо обхід
    if traversal_type == 'bfs':
        visited_order = bfs_traversal(root)
        title = "Обхід у ШИРИНУ (BFS) - використовує ЧЕРГУ"
    else:
        visited_order = dfs_traversal(root)
        title = "Обхід у ГЛИБИНУ (DFS) - використовує СТЕК"
    
    # Генеруємо кольори від темного до світлого
    colors = generate_colors(len(visited_order))
    
    # Призначаємо кольори вузлам у порядку відвідування
    for i, node in enumerate(visited_order):
        node.color = colors[i]
    
    # Виводимо порядок обходу
    order = [node.val for node in visited_order]
    print(f"\n{title}")
    print(f"Порядок відвідування: {order}")
    print(f"Кольори змінюються від темного {colors[0]} до світлого {colors[-1]}\n")
    
    # Малюємо дерево
    draw_tree(root, title=title)


# -------------------- Створення дерева з масиву --------------------

def create_tree_from_array(arr):
    """Створює бінарне дерево з масиву"""
    if not arr:
        return None
    
    nodes = [Node(val) for val in arr]
    
    for i in range(len(arr)):
        left_idx = 2 * i + 1
        right_idx = 2 * i + 2
        
        if left_idx < len(arr):
            nodes[i].left = nodes[left_idx]
        if right_idx < len(arr):
            nodes[i].right = nodes[right_idx]
    
    return nodes[0]


# -------------------- ГОЛОВНА ПРОГРАМА --------------------

if __name__ == "__main__":
    # Створюємо дерево
    tree_array = [0, 4, 1, 5, 10, 3]
    root = create_tree_from_array(tree_array)
    
    print("=" * 60)
    print("ВІЗУАЛІЗАЦІЯ ОБХОДУ БІНАРНОГО ДЕРЕВА")
    print("=" * 60)
    print(f"Дерево побудовано з масиву: {tree_array}")
    
    # Обхід у ширину (BFS)
    visualize_traversal(root, traversal_type='bfs')
    
    # Створюємо дерево знову (бо кольори змінилися)
    root = create_tree_from_array(tree_array)
    
    # Обхід у глибину (DFS)
    visualize_traversal(root, traversal_type='dfs')
    
    # -------------------- ДОДАТКОВИЙ ПРИКЛАД --------------------
    
    print("\n" + "=" * 60)
    print("ДОДАТКОВИЙ ПРИКЛАД: Більше дерево")
    print("=" * 60)
    
    large_tree = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    root2 = create_tree_from_array(large_tree)
    print(f"Дерево побудовано з масиву: {large_tree}")
    
    # BFS
    visualize_traversal(root2, traversal_type='bfs')
    
    # DFS
    root2 = create_tree_from_array(large_tree)
    visualize_traversal(root2, traversal_type='dfs')