# Classe baseada na estrutura de lista duplamente encadeada mostrada em aula e anexada na atividade

class DoublyLinkedList:
    
    class _DoublyNode:
        def __init__(self, elem, prev, next):
            self._elem = elem
            self._prev = prev
            self._next = next
            
        @property
        def elem(self):
            return self._elem

        @elem.setter
        def elem(self, elem):
            self._elem = elem

        @property
        def prev(self):
            return self._prev

        @prev.setter
        def prev(self, node):
            self._prev = node

        @property
        def next(self):
            return self._next

        @next.setter
        def next(self, node):
            self._next = node
    
    def __init__(self):
        self._header = self._DoublyNode(None, None, None)
        self._trailer = self._DoublyNode(None, None, None)
        self._header.next = self._trailer
        self._trailer.prev = self._header
        self._length = 0
        self._cursor = None
        
    def __len__(self):
        return self._length
    
    def append(self, elem):
       
        last_node = self._trailer.prev
            
        node = self._DoublyNode(elem, last_node, self._trailer)
            
        last_node.next = node
        self._trailer.prev = node
        
        self._length += 1
        
        if (self._cursor is None):
            self._cursor = node
            
    def play_next(self):
        if (self._cursor and self._cursor.next is not self._trailer):
            self._cursor = self._cursor.next
            return self.current()
        return None
        
    def play_prev(self):
        if (self._cursor and self._cursor.prev is not self._header):
            self._cursor = self._cursor.prev
            return self.current()
        return None
    
    def current(self):
        if self._cursor:
            return self._cursor.elem
        return None
    
    def reset_cursor(self):
        if self._cursor:
            self._cursor = self._header.next
        
    def remove_at(self, pos):
        node = self._header.next
        
        for n in range(pos):
            node = node.next
            
        if (node == self._cursor):
            if (node.next is not self._trailer):
                self._cursor = node.next
            elif (node.prev is not self._header):
                self._cursor = node.prev
            else:
                self._cursor = None
                        
        node.prev.next = node.next
        node.next.prev = node.prev
        
        self._length -= 1
        return node.elem
    
    def __iter__(self):
        current = self._header.next
        
        while (current is not self._trailer):
            yield current.elem
            current = current.next 
    