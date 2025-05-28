from abc import ABC, abstractmethod

class Shape(ABC): # Inherit from ABC
    @abstractmethod # This method MUST be implemented by subclasses
    def area(self):
        pass # No implementation here

    @abstractmethod # Another abstract method
    def perimeter(self):
        pass

    def get_description(self): # Concrete method (has implementation)
        return "This is a geometric shape."

# This would raise a TypeError because it's abstract:
# my_shape = Shape()

class Circle(Shape): # Must implement area and perimeter
    def __init__(self, radius):
        self.radius = radius

    def area(self): # Implements abstract method
        return 3.14 * self.radius ** 2

    def perimeter(self): # Implements abstract method
        return 2 * 3.14 * self.radius

class Square(Shape):
    def __init__(self, side):
        self.side = side

    def area(self): # Implements abstract method
        return self.side ** 2

    def perimeter(self): # Implements abstract method
        return 4 * self.side

c = Circle(5)
s = Square(4)

shapes = [c, s]
for shape in shapes:
    print(f"Shape: {shape.get_description()}, Area: {shape.area()}, Perimeter: {shape.perimeter()}")