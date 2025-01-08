class Node:
    def __init__(self, id, data):
        self.id = id
        self.data = data
        self.next = None       
 
class LinkedList:
    def __init__(self):
        self.head = None
        self.length = 0
 
    def add(self, id, data):
        new_node = Node(id, data)
        if self.head is None:
            self.head = new_node
            self.length += 1 
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
            self.length += 1
 
    def find(self, id):
        current = self.head
        while current:
            if current.id == id:
                return current.data
            current = current.next
        return None
 
    def delete(self, id):
        if self.head is None:
            return
        if self.head.id == id:
            self.head = self.head.next
            self.length -= 1 
            return
        current = self.head
        while current.next:
            if current.next.id == id:
                current.next = current.next.next
                self.length -= 1 
                return
            current = current.next