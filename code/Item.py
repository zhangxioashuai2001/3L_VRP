from typing import List


class Item:
    def __init__(self, x=None, y=None, z=None, length=None, width=None, height=None, fragile=None):
        self.x = x
        self.y = y
        self.z = z
        self.length = length
        self.width = width
        self.height = height
        self.orientation = 0
        self.visit_order = 0  # visit_order小的表示先被送到
        self.fragile = fragile  # fragile = 0 表示没有fragile特性， 1 表示有fragile 特性

    @classmethod
    def from_coordinates_and_dimensions(cls, x, y, z, length, width, height):
        return cls(x, y, z, length, width, height)

    @classmethod
    def from_dimensions(cls, length, width, height):
        return cls(None, None, None, length, width, height)

    @classmethod
    def from_dimensions_and_fragile(cls, length, width, height, fragile):
        return cls(None, None, None, length, width, height, fragile)

    def get_dimensions(self):
        if self.orientation == 0:
            return self.length, self.width, self.height
        elif self.orientation == 1:
            return self.width, self.length, self.height
        elif self.orientation == 2:
            return self.height, self.length, self.width
        elif self.orientation == 3:
            return self.height, self.width, self.length
        elif self.orientation == 4:
            return self.width, self.height, self.length
        elif self.orientation == 5:
            return self.length, self.height, self.width

    def __eq__(self, other):
        return (self.x, self.y, self.z, self.length, self.width, self.height, self.orientation, self.visit_order,
                self.fragile) == (
                   other.x, other.y, other.z, other.length, other.width, other.height, other.orientation,
                   other.visit_order, other.fragile)

    def __hash__(self):
        return hash((self.x, self.y, self.z, self.length, self.width, self.height, self.orientation, self.visit_order,
                     self.fragile))

    def __repr__(self):
        return f"Item(x={self.x}, y={self.y}, z={self.z}, length={self.length}, width={self.width}, height={self.height}, orientation={self.orientation}, visit_order={self.visit_order}, fragile={self.fragile})"


def items_overlap(item1, item2):
    l1, w1, h1 = item1.get_dimensions()
    l2, w2, h2 = item2.get_dimensions()
    if (item1.x + l1 <= item2.x or item1.x >= item2.x + l2 or
            item1.y + w1 <= item2.y or item1.y >= item2.y + w2 or
            item1.z + h1 <= item2.z or item1.z >= item2.z + h2):
        return False
    return True


# 对items 进行排序， 1. lifo； 2. non-fragile在前； 3.按体积降序排序
def sort_items(items: List[Item]) -> None:
    items.sort(key=lambda item: (-item.visit_order, item.fragile, -item.length * item.width * item.height))

