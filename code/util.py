from Item import Item, items_overlap


# 计算两个物体间的上下面接触面积
def cal_bottomtop_touching_area(item1, item2) -> int:
    x1, y1, z1 = item1.x, item1.y, item1.z
    x2, y2, z2 = item2.x, item2.y, item2.z
    l1, w1, h1 = item1.get_dimensions()
    l2, w2, h2 = item2.get_dimensions()
    a = calculate_intersection(x1, x1 + l1, x2, x2 + l2)
    b = calculate_intersection(y1, y1 + w1, y2, y2 + w2)
    A1q, A2q, A3q, A4q = 0, 0, 0, 0
    # 计算 A1q
    if y2 < y1 + w1:
        A1q = (y1 + w1 - y2) * a
    # 计算 A2q
    if y2 < y1:
        A2q = (y1 - y2) * a
    # 计算 A3q
    if y2 + w2 < y1 + w1:
        A3q = (y1 + w1 - y2 - w2) * a
    # 计算 A4q
    if y2 + w2 < y1:
        A4q = (y1 - y2 - w2) * a
    s = A1q + A2q + A3q + A4q
    return a * b


# 计算两个物体间的左右面接触面积
def cal_leftright_touching_area(item1, item2) -> int:
    x1, y1, z1 = item1.x, item1.y, item1.z
    x2, y2, z2 = item2.x, item2.y, item2.z
    l1, w1, h1 = item1.get_dimensions()
    l2, w2, h2 = item2.get_dimensions()
    a = calculate_intersection(z1, z1 + h1, z2, z2 + h2)
    b = calculate_intersection(x1, x1 + l1, x2, x2 + l2)
    A1q, A2q, A3q, A4q = 0, 0, 0, 0
    # 计算 A1q
    if x2 < x1 + l1:
        A1q = (x1 + l1 - x2) * a
    # 计算 A2q
    if x2 < x1:
        A2q = (x1 - x2) * a
    # 计算 A3q
    if x2 + l2 < x1 + l1:
        A3q = (x1 + l1 - x2 - l2) * a
    # 计算 A4q
    if x2 + l2 < x1:
        A4q = (x1 - x2 - l2) * a
    s = A1q + A2q + A3q + A4q
    return a * b


# 计算两个物体间的前后面接触面积
def cal_frontback_touching_area(item1, item2) -> int:
    x1, y1, z1 = item1.x, item1.y, item1.z
    x2, y2, z2 = item2.x, item2.y, item2.z
    l1, w1, h1 = item1.get_dimensions()
    l2, w2, h2 = item2.get_dimensions()
    a = calculate_intersection(z1, z1 + h1, z2, z2 + h2)
    b = calculate_intersection(y1, y1 + w1, y2, y2 + w2)
    A1q, A2q, A3q, A4q = 0, 0, 0, 0
    # 计算 A1q
    if y2 < y1 + w1:
        A1q = (y1 + w1 - y2) * a
    # 计算 A2q
    if y2 < y1:
        A2q = (y1 - y2) * a
    # 计算 A3q
    if y2 + w2 < y1 + w1:
        A3q = (y1 + w1 - y2 - w2) * a
    # 计算 A4q
    if y2 + w2 < y1:
        A4q = (y1 - y2 - w2) * a
    s = A1q + A2q + A3q + A4q
    return a * b


# 求交集
def calculate_intersection(z1, Dz1, z2, Dz2) -> int:
    # 区间 [z1, z1+Dz1]
    start1 = z1
    end1 = Dz1

    # 区间 [z2, z2+Dz2]
    start2 = z2
    end2 = Dz2

    # 计算交集
    intersection_start = max(start1, start2)
    intersection_end = min(end1, end2)

    # 如果没有交集，交集长度为 0
    if intersection_start >= intersection_end:
        intersection_length = 0
    else:
        intersection_length = intersection_end - intersection_start

    return intersection_length


# 先被送到的物体（item1，也是现在要装的物体)）不可以被后来送到的物体(item2,也是先装载好的物体)压在下面或者堵在前面，左右贴上是ok的，
def is_lifo_satisfied(item1: Item, item2: Item) -> bool:
    # 如果 item1 在 item之后或者同样优先级，则item2不会挡item1
    if item1.visit_order >= item2.visit_order:
        return True
    # 前后堵塞： y-z平面上投影有交集，并且x轴方向上 item1 在items前面
    x1, y1, z1 = item1.x, item1.y, item1.z
    x2, y2, z2 = item2.x, item2.y, item2.z
    l1, w1, h1 = item1.get_dimensions()
    l2, w2, h2 = item2.get_dimensions()
    a_zy = calculate_intersection(z1, z1 + h1, z2, z2 + h2)
    b_zy = calculate_intersection(y1, y1 + w1, y2, y2 + w2)
    if a_zy * b_zy > 0 and x1 + l1 <= x2:
        return False
    # 上下堵塞： x-y平面上投影有交集，并且z轴方向上 item1 在items下面
    a_xy = calculate_intersection(y1, y1 + w1, y2, y2 + w2)
    b_xy = calculate_intersection(x1, x1 + l1, x2, x2 + l2)
    if a_xy * b_xy > 0 and z1 + h1 <= z2:
        return False
    return True


# item1 如果放在item2的上面，则计算一个s_q,表示由item2 提供给item1 的支持
def cal_supportarea(item1, item2) -> float:
    x1, y1, z1 = item1.x, item1.y, item1.z
    x2, y2, z2 = item2.x, item2.y, item2.z
    l1, w1, h1 = item1.get_dimensions()
    l2, w2, h2 = item2.get_dimensions()
    if not z1 == z2 + h2:
        return 0
    a_xy = calculate_intersection(y1, y1 + w1, y2, y2 + w2)
    b_xy = calculate_intersection(x1, x1 + l1, x2, x2 + l2)
    s_q : float = a_xy * b_xy
    return s_q

# item1 如果是fragile,则不能被放在非fragile的物体下面，但如果item2也是fragile 则可以，反过来同理
def is_fragile_satisfied(item1:Item, item2: Item) -> bool:
    #二者都是fragile或者都是non_fragile，则返回 true
    if item1.fragile == item2.fragile:
        return True

    x1, y1, z1 = item1.x, item1.y, item1.z
    x2, y2, z2 = item2.x, item2.y, item2.z
    l1, w1, h1 = item1.get_dimensions()
    l2, w2, h2 = item2.get_dimensions()

    # 如果item1 易碎，则不能放在item2 下面
    if item1.fragile ==1 and item2.fragile ==0:
        if not z1 + h1 == z2:
            return True
        a_xy = calculate_intersection(y1, y1 + w1, y2, y2 + w2)
        b_xy = calculate_intersection(x1, x1 + l1, x2, x2 + l2)
        if a_xy*b_xy>0:
            return False
        return True
    if item1.fragile == 0 and item2.fragile == 1:
        if not z1  == z2 + h2:
            return True
        a_xy = calculate_intersection(y1, y1 + w1, y2, y2 + w2)
        b_xy = calculate_intersection(x1, x1 + l1, x2, x2 + l2)
        if a_xy * b_xy > 0:
            return False
        return  True

def slide_item(item, container_length, container_width, container_height, placed_items):
    l, w, h = item.get_dimensions()
    # Slide to the back (x-axis)
    while item.x > 0:
        item.x -= 0.1
        if item.x < 0 or any(items_overlap(item, other) for other in placed_items):
            item.x += 0.1
            break
    # Slide to the bottom (z-axis)
    while item.z > 0:
        item.z -= 0.1
        if item.z < 0 or any(items_overlap(item, other) for other in placed_items):
            item.z += 0.1
            break
    # Slide to the left (y-axis)
    while item.y > 0:
        item.y -= 0.01
        if item.y < 0 or any(items_overlap(item, other) for other in placed_items):
            item.y += 0.01
            break

# 二分法查找一个方向上最大可以滑动距离
def find_max_slide_distance(item, direction,placed_items)->float:
    low, high = 0.0, 1.0
    while can_slide(high,item,placed_items,direction):
        low = high
        high *=  2

    while high - low > 1e-3:  # Use a small epsilon for precision
        mid = (low + high) / 2
        if can_slide(mid,item,placed_items,direction):
            low = mid
        else:
            high = mid
    return low

def can_slide(dist,item,placed_items,direction)->bool:
    if direction == 'x':
        item.x -= dist
    elif direction == 'y':
        item.y -= dist
    elif direction == 'z':
        item.z -= dist

    for other in placed_items:
        if items_overlap(item, other):
            if direction == 'x':
                item.x += dist
            elif direction == 'y':
                item.y += dist
            elif direction == 'z':
                item.z += dist
            return False

    if direction == 'x' and item.x < 0:
        item.x += dist
        return False
    if direction == 'y' and item.y < 0:
        item.y += dist
        return False
    if direction == 'z' and item.z < 0:
        item.z += dist
        return False

    if direction == 'x':
        item.x += dist
    elif direction == 'y':
        item.y += dist
    elif direction == 'z':
        item.z += dist

    return True