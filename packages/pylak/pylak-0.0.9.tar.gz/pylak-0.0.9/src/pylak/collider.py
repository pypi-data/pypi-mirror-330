
from .visual import Rectangle

###########################################
# Collider 
###########################################
class Collider:
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = Rectangle(width, height, color=(0, 135, 0))


    def draw(self):
        self.rect.draw(self.x, self.y)


    def isColliding(self, other):
        isColliding = not (self.x + self.width < other.x or
                self.x > other.x + other.width or
                self.y + self.height < other.y or
                self.y > other.y + other.height)

        if isColliding:
            self.rect.color = (91, 124, 221)
        else:
            self.rect.color = (12, 172, 89)
        
        other.rect.color = self.rect.color

        return isColliding
