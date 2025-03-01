class StaticArray:
    def __init__(self, n):
        self.data = []*n
    
    def get_at(self,i):
        if not(0 <= i < len(self.data)) : raise IndexError
        return self.data[i]
    def set_at(self, i, x):
        if not(0 <= i < len(self.data)) : raise IndexError
        self.data = x