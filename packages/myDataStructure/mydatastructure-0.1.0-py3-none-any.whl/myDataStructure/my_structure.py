class MyDataStructure:
    def __init__(self):
        self.data = []

    def add(self, value):
        """Add an element to the structure."""
        self.data.append(value)

    def remove(self, value):
        """Remove an element if it exists."""
        if value in self.data:
            self.data.remove(value)

    def display(self):
        """Print all elements."""
        return self.data
