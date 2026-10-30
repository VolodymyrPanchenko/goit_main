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

    # пошук мінімального елемента
    def find_min(self):
        if self.root is None:
            return None
        cur = self.root
        while cur.left:
            cur = cur.left
        return cur.key


# приклад використання
bst = BST()
for v in [50, 30, 70, 20, 40, 19, 80]:
    bst.insert(v)

print("Мінімум в дереві:", bst.find_min())
