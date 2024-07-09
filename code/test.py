import unittest
from copy import deepcopy
from Item import Item, sort_items
from util import cal_bottomtop_touching_area,is_lifo_satisfied,cal_supportarea,calculate_intersection, is_fragile_satisfied,find_max_slide_distance

class TestCalBottomTopTouchingArea(unittest.TestCase):

    def test_partial_overlap(self):
        item1 = Item(0, 0, 0, 10, 10, 10)
        item1.orientation =0
        item2 = Item(6, 5, 0, 10, 10, 10)
        item2.orientation =0
        result = cal_bottomtop_touching_area(item1, item2)
        expected = (4 * 5)  # 根据你的逻辑填写预期结果
        self.assertEqual(result, expected)

    def test_no_overlap(self):
        item1 = Item(0, 0, 0, 10, 10, 10)
        item2 = Item(0, 15, 0, 10, 10, 10)
        result = cal_bottomtop_touching_area(item1, item2)
        expected = 0  # 根据你的逻辑填写预期结果
        self.assertEqual(result, expected)

    def test_edge_overlap(self):
        item1 = Item(0, 0, 0, 10, 10, 10)
        item2 = Item(10, 0, 0, 10, 10, 10)
        result = cal_bottomtop_touching_area(item1, item2)
        expected = 0  # 根据你的逻辑填写预期结果
        self.assertEqual(result, expected)

    #测试lifo约束的前后方向
    def test_is_lifo_satisfied(self):
        item1 = Item(0, 0, 0, 2, 2, 2)
        item1.visit_order = 1
        item2 = Item(3, 0, 0, 2, 2, 2)
        item2.visit_order =2
        assert is_lifo_satisfied(item1, item2) == False, "测试1失败"

    # 测试lifo约束的上下方向
    def test_is_lifo_satisfied(self):
        item1 = Item(0, 0, 0, 2, 2, 2)
        item1.visit_order = 1
        item2 = Item(1, 0, 3, 2, 1, 2)
        item2.visit_order = 2
        assert is_lifo_satisfied(item1, item2) == False, "测试1失败"

    #测试lifo约束的左右方向
    def test_is_lifo_satisfied(self):
        item1 = Item(0, 0, 0, 2, 2, 2)
        item1.visit_order = 1
        item2 = Item(1, 2, 0, 2, 2, 2)
        item2.visit_order =2
        assert is_lifo_satisfied(item1, item2) == True, "测试1失败"

    #测试lifo约束的满足约束的情况
    def test_is_lifo_satisfied(self):
        item1 = Item(0, 0, 0, 2, 2, 2)
        item1.visit_order = 1
        item2 = Item(3, 3, 5, 2, 2, 2)
        item2.visit_order =2
        assert is_lifo_satisfied(item1, item2) == True, "测试1失败"

    # 测试support_area 函数
    def test_cal_supportaera(self):
        item1 = Item(1, 1, 2, 2, 2, 2)

        item2 = Item(0, 0, 0, 4, 4, 2)
        assert cal_supportarea(item1, item2) == 4, "测试1失败"

    # 测试 cal_intersection
    def test_calculate_intersection(self):
        # Test cases: (inputs, expected_output)
        test_cases = [
            ((1, 2, 3, 4), 0),  # No overlap
            ((1, 3, 2, 4), 1),  # Partial overlap
            ((1, 4, 2, 2), 0),  # One inside the other
            ((1, 4, 1, 4), 3),  # Exactly same
            ((2, 2, 1, 4), 0),  # One inside the other (different order)
            ((3, 2, 1, 4), 0),  # Overlap at the end
            ((1, 3, 2, 1), 0)  # Partial overlap (one unit)
        ]

        for i, (inputs, expected) in enumerate(test_cases):
            result = calculate_intersection(*inputs)
            assert result == expected, f"Test case {i + 1} failed: {inputs} -> {result} (expected: {expected})"
            print(f"Test case {i + 1} passed")

    def test_is_fragile_satisfied(self):
        # Test cases: (item1, item2, expected_output)
        test_cases = [
            (Item(0, 0, 0, 2, 2, 2, 0), Item(0, 0, 2, 2, 2, 2, 1), True),  # fragile on non-fragile, overlap
            (Item(0, 0, 0, 2, 2, 2, 0), Item(2, 2, 2, 2, 2, 2, 1), True),  # fragile on non-fragile, overlap
            (Item(0, 0, 2, 2, 2, 2, 0), Item(0, 0, 0, 2, 2, 2, 1), False),  # non-fragile on fragile, overlap
            (Item(2, 2, 2, 2, 2, 2, 0), Item(0, 0, 0, 2, 2, 2, 1), True),  # non-fragile on fragile, overlap
            (Item(0, 0, 0, 2, 2, 2, 1), Item(0, 0, 2, 2, 2, 2, 1), True),  # fragile on fragile
            (Item(0, 0, 0, 2, 2, 2, 0), Item(0, 0, 2, 2, 2, 2, 0), True)  # non-fragile on non-fragile
        ]

        for i, (item1, item2, expected) in enumerate(test_cases):
            result = is_fragile_satisfied(item1, item2)
            assert result == expected, f"Test case {i + 1} failed: {item1.__dict__}, {item2.__dict__} -> {result} (expected: {expected})"
            print(f"Test case {i + 1} passed")


    # 测试items的排序是否正确
    def test_sort_items(self):
        # 创建一些 Item 对象
        items = [
            Item(length=10, width=5, height=5, fragile=0),
            Item(length=8, width=5, height=5, fragile=1),
            Item(length=6, width=5, height=5, fragile=0),
            Item(length=4, width=5, height=5, fragile=1),
            Item(length=7, width=7, height=7, fragile=0)
        ]

        # 为每个 Item 对象设置 visit_order
        items[0].visit_order = 3  # item 0
        items[1].visit_order = 2  # item 1
        items[2].visit_order = 1  # item 2
        items[3].visit_order = 1  # item 3
        items[4].visit_order = 2  # item 4
        # 定义预期的排序结果
        expected_order = [
            deepcopy(items[0]),  # visit_order 3, fragile 0, volume 250
            deepcopy(items[4]),  # visit_order 2, fragile 0, volume 343
            deepcopy(items[1]),  # visit_order 2, fragile 1, volume 200
            deepcopy(items[2]),  # visit_order 1, fragile 0, volume 150
            deepcopy(items[3])  # visit_order 1, fragile 1, volume 100
        ]
        # 调用 sort_items 函数进行排序
        sort_items(items)



        # 检查排序结果是否符合预期
        for i, item in enumerate(items):
            self.assertEqual(item, expected_order[i])

    def test_find_max_slide_distance(self):
        # 创建一些 Item 实例
        # 车厢 10 * 5 * 5
        itemleft = Item.from_dimensions(10, 0, 5)
        itembottom = Item.from_dimensions(0, 5, 5)
        itemback = Item.from_dimensions(10, 5, 0)
        item1 = Item.from_dimensions(2.98, 3, 3)
        item2 = Item.from_dimensions(1.28, 2, 2)
        item3 = Item.from_dimensions(2, 2, 2)

        # 设置初始位置
        itemleft.x, itemleft.y, itemleft.z = 0, 0, 0
        itembottom.x, itembottom.y, itembottom.z = 0, 0, 0
        itemback.x, itemback.y, itemback.z = 0, 0, 0
        item1.x, item1.y, item1.z = 0, 0, 0
        item2.x, item2.y, item2.z = 0, 3, 0
        item3.x, item3.y, item3.z = 3.0, 3, 0

        # 放置的物品列表
        placed_items = [item1, item2,itemleft,itemback,itembottom]


        # 测试 item3 在 x, y, z 方向上的最大滑动距离
        slide_distance_x = find_max_slide_distance(item3, 'x', placed_items)
        item3.x -= slide_distance_x
        slide_distance_y = find_max_slide_distance(item3, 'y', placed_items)
        slide_distance_z = find_max_slide_distance(item3, 'z', placed_items)
        self.assertAlmostEqual(slide_distance_x, 1.72, places=5)
        self.assertAlmostEqual(slide_distance_y, 0, places=5)
        self.assertAlmostEqual(slide_distance_z, 0, places=5)
        print(f"Item3 can slide in x direction by: {slide_distance_x} units")
        print(f"Item3 can slide in y direction by: {slide_distance_y} units")
        print(f"Item3 can slide in z direction by: {slide_distance_z} units")

if __name__ == '__main__':
    unittest.main()
