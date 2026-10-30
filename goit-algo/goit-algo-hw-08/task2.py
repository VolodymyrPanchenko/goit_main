class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, key):
        if self.root is None:
            self.root = Node(key)
            return
        cur = self.root
        while True:
            if key < cur.key:
                if cur.left is None:
                    cur.left = Node(key)
                    return
                cur = cur.left
            else:
                if cur.right is None:
                    cur.right = Node(key)
                    return
                cur = cur.right

    def sum_tree(self):
        if self.root is None:  # обробка порожнього дерева
            return 0
        total = 0
        stack = [self.root]
        while stack:
            node = stack.pop()
            if node is None:
                continue    
            total += node.key
            stack.append(node.left)
            stack.append(node.right)
        return total


# приклад
bst = BST()
for k in [5, 3, 7, 2, 4, 6, 8]:
    bst.insert(k)

print(bst.sum_tree())  
