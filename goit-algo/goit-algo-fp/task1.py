class Node:
    """Клас вузла однозв’язного списку"""
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    """Клас однозв’язного списку"""
    def __init__(self):
        self.head = None

    def append(self, data):
        """Додати елемент у кінець списку"""
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        curr = self.head
        while curr.next:
            curr = curr.next
        curr.next = new_node

    def print_list(self):
        """Вивести список"""
        curr = self.head
        elements = []
        while curr:
            elements.append(curr.data)
            curr = curr.next
        print(elements)

    def reverse(self):
        """Реверсування списку"""
        prev = None
        curr = self.head
        while curr:
            next_node = curr.next
            curr.next = prev
            prev = curr
            curr = next_node
        self.head = prev

    def insertion_sort(self):
        """Сортування вставками для однозв’язного списку"""
        sorted_head = None  # початок відсортованого списку
        curr = self.head
        while curr:
            next_node = curr.next  # зберігаємо наступний елемент
            sorted_head = self._sorted_insert(sorted_head, curr)
            curr = next_node
        self.head = sorted_head

    def _sorted_insert(self, head, node):
        """Допоміжна функція для вставки вузла у відсортований список"""
        if head is None or node.data < head.data:
            node.next = head
            return node
        curr = head
        while curr.next and curr.next.data < node.data:
            curr = curr.next
        node.next = curr.next
        curr.next = node
        return head


def merge_two_sorted_lists(l1, l2):
    """Функція об’єднання двох відсортованих списків"""
    dummy = Node(0)
    tail = dummy
    a = l1.head
    b = l2.head
    while a and b:
        if a.data < b.data:
            tail.next = a
            a = a.next
        else:
            tail.next = b
            b = b.next
        tail = tail.next
    tail.next = a or b
    result = LinkedList()
    result.head = dummy.next
    return result


# === Приклад використання ===
if __name__ == "__main__":
    print("=== Початковий список ===")
    lst = LinkedList()
    for x in [5, 2, 8, 1, 3]:
        lst.append(x)
    lst.print_list()

    print("\n=== Реверс ===")
    lst.reverse()
    lst.print_list()

    print("\n=== Сортування вставками ===")
    lst.insertion_sort()
    lst.print_list()

    print("\n=== Об’єднання двох відсортованих списків ===")
    list1 = LinkedList()
    for x in [1, 4, 7]:
        list1.append(x)
    list2 = LinkedList()
    for x in [2, 3, 9]:
        list2.append(x)
    merged = merge_two_sorted_lists(list1, list2)
    merged.print_list()
