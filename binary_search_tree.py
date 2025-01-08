class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
 
class BST:
    def __init__(self):
        self.root = None
 
    def insert(self, key, value):
        if self.root is None:
            self.root = Node(key, value)
        else:
            self._insert(self.root, key, value)
 
    def _insert(self, current, key, value):
        if key < current.key:
            if current.left is None:
                current.left = Node(key, value)
            else:
                self._insert(current.left, key, value)
        elif key > current.key:
            if current.right is None:
                current.right = Node(key, value)
            else:
                self._insert(current.right, key, value)
        else:
            raise ValueError("Duplicate keys are not allowed.")
 
    def search(self, key):
        return self._search(self.root, key)
 
    def _search(self, current, key):
        if current is None:
            return None
        if key == current.key:
            return current.value
        elif key < current.key:
            return self._search(current.left, key)
        else:
            return self._search(current.right, key)
