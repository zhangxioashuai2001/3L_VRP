def parse_vrp_file(file_path):
    """
    解析给定路径的VRP问题文本文件，并返回解析后的数据。

    参数:
    file_path (str): 文本文件的路径。

    返回:
    dict: 解析后的数据，包括基本信息、车辆尺寸、节点和箱子类型、距离。
    """
    general_info = {}
    vehicle_dimensions = {}
    nodes = []
    distances = []

    with open(file_path, 'r') as file:
        lines = file.readlines()

    # 清理注释行和空行
    lines = [line.strip() for line in lines if line.strip() and not line.strip().startswith('//')]

    # 跳过文件头部不相关的行
    index = 1  # 从第2行开始（第1行是文件编号）

    # 解析基本信息
    general_info = {
        'num_customers': int(lines[index].split()[0]),
        'num_vehicles': int(lines[index].split()[1]),
        'num_box_types': int(lines[index].split()[2]),
        'num_items': int(lines[index].split()[3])
    }

    # 解析车辆尺寸
    index += 1
    vehicle_dimensions = {
        'max_weight': int(lines[index].split()[0]),
        'height': int(lines[index].split()[1]),
        'width': int(lines[index].split()[2]),
        'length': int(lines[index].split()[3])
    }

    # 解析节点和箱子类型
    index += 1
    while index < len(lines):
        line = lines[index]
        parts = line.split()
        if len(parts) == 2:
            node = int(parts[0])
            num_boxes = int(parts[1])
            boxes = []
            for _ in range(num_boxes):
                index += 1
                parts = lines[index].split()
                h, w, l = map(int, parts[:3])
                no_boxes, frag, weight = map(int, parts[3:])
                boxes.append({
                    'height': h,
                    'width': w,
                    'length': l,
                    'no_boxes': no_boxes,
                    'fragile': frag,
                    'weight': weight
                })
            nodes.append({
                'node': node,
                'boxes': boxes
            })
            index += 1
        else:
            break

    # 解析距离
    distance_dict = {}
    while index < len(lines):
        line = lines[index]
        parts = line.split()
        if len(parts) == 3:
            node1, node2, distance = int(parts[0]), int(parts[1]), float(parts[2])
            if node1 not in distance_dict:
                distance_dict[node1] = []
            distance_dict[node1].append({
                'node2': node2,
                'distance': distance
            })
        index += 1

    # 将距离字典转为列表形式
    for node1, values in distance_dict.items():
        for value in values:
            distances.append({
                'node1': node1,
                'node2': value['node2'],
                'distance': value['distance']
            })

    return {
        'general_info': general_info,
        'vehicle_dimensions': vehicle_dimensions,
        'nodes': nodes,
        'distances': distances
    }


# # 使用示例
# file_path = 'D:/OneDrive - stu.hit.edu.cn/桌面/3L_VRP/code/vrp/by_01.txt'
# parsed_data = parse_vrp_file(file_path)
#
# print("基本信息:", parsed_data['general_info'])
# print("车辆尺寸:", parsed_data['vehicle_dimensions'])
# print("节点和箱子类型:", parsed_data['nodes'])
#
# # 打印距离
# for distance in parsed_data['distances']:
#     print(f"距离: {distance['node1']} -> {distance['node2']}: {distance['distance']}")