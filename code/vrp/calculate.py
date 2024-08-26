import random
from data_read import parse_vrp_file


def calculate_total_distance(routes, distances):
    """
    计算给定路径的总距离。

    参数:
    routes (list of lists): 每辆车的路径列表。
    distances (list of dicts): 节点之间的距离数据。

    返回:
    float: 总距离。
    """
    distance_map = {(d['node1'], d['node2']): d['distance'] for d in distances}
    total_distance = 0

    for route in routes:
        for i in range(len(route) - 1):
            total_distance += distance_map.get((route[i], route[i + 1]), 0)

    return total_distance


# def swap_operator(routes, distances):
#     """
#     在不同路径之间交换两个节点。
#
#     参数:
#     routes (list of lists): 每辆车的路径列表。
#     distances (list of dicts): 节点之间的距离数据。
#
#     返回:
#     tuple: 最优路径和对应的总距离。
#     """
#     best_routes = [route[:] for route in routes]
#     best_distance = calculate_total_distance(best_routes, distances)
#
#     num_routes = len(routes)
#
#     for i in range(num_routes):
#         for j in range(i + 1, num_routes):
#             for node_i in range(len(routes[i])):
#                 for node_j in range(len(routes[j])):
#                     # 交换节点
#                     new_routes = [r[:] if r != routes[i] and r != routes[j] else r[:] for r in routes]
#                     new_routes[i][node_i], new_routes[j][node_j] = new_routes[j][node_j], new_routes[i][node_i]
#
#                     # 计算新路径的总距离
#                     new_distance = calculate_total_distance(new_routes, distances)
#
#                     # 更新最优解
#                     if new_distance < best_distance:
#                         best_routes = new_routes
#                         best_distance = new_distance
#
#     return best_routes, best_distance
def swap_operator(routes, distances):
    """
    在不同路径之间交换两个节点，同时确保每条路径的起点和终点都是0。

    参数:
    routes (list of lists): 每辆车的路径列表。
    distances (list of dicts): 节点之间的距离数据。

    返回:
    tuple: 最优路径和对应的总距离。
    """
    best_routes = [route[:] for route in routes]
    best_distance = calculate_total_distance(best_routes, distances)

    num_routes = len(routes)

    for i in range(num_routes):
        for j in range(i + 1, num_routes):
            # 排除起点和终点
            route1_nodes = [node for node in routes[i] if node != 0]
            route2_nodes = [node for node in routes[j] if node != 0]

            if len(route1_nodes) < 2 or len(route2_nodes) < 2:
                continue

            for node_i in range(len(route1_nodes)):
                for node_j in range(len(route2_nodes)):
                    # 交换节点
                    new_route1 = route1_nodes[:]
                    new_route2 = route2_nodes[:]

                    # 交换节点位置
                    new_route1[node_i], new_route2[node_j] = new_route2[node_j], new_route1[node_i]

                    # 修复路径，确保起点和终点都是0
                    new_route1 = [0] + new_route1 + [0]
                    new_route2 = [0] + new_route2 + [0]

                    new_routes = [new_route1 if k == i else new_route2 if k == j else routes[k] for k in range(num_routes)]
                    new_distance = calculate_total_distance(new_routes, distances)

                    # 更新最优解
                    if new_distance < best_distance:
                        best_routes = new_routes
                        best_distance = new_distance

    return best_routes, best_distance


# def relocate_operator(route, distances):
#     """
#     在单条路径内移动一个节点到另一个位置。
#
#     参数:
#     route (list): 单辆车的路径。
#     distances (list of dicts): 节点之间的距离数据。
#
#     返回:
#     tuple: 最优路径和对应的总距离。
#     """
#     best_route = route[:]
#     best_distance = calculate_total_distance([best_route], distances)
#
#     for i in range(len(route)):
#         for j in range(len(route)):
#             if i != j:
#                 # 重新安置节点
#                 node = best_route.pop(i)
#                 best_route.insert(j, node)
#
#                 # 计算新路径的总距离
#                 new_distance = calculate_total_distance([best_route], distances)
#
#                 # 更新最优解
#                 if new_distance < best_distance:
#                     best_route = best_route[:]
#                     best_distance = new_distance
#
#     return best_route, best_distance
def relocate_operator(route, distances):
    """
    在单条路径内移动一个节点到另一个位置，同时确保移动的节点和目标位置都不是起点或终点。

    参数:
    route (list): 单辆车的路径。
    distances (list of dicts): 节点之间的距离数据。

    返回:
    tuple: 最优路径和对应的总距离。
    """
    best_route = route[:]
    best_distance = calculate_total_distance([best_route], distances)

    # 排除起点和终点的索引
    valid_indices = list(range(1, len(route) - 1))

    for i in valid_indices:
        for j in valid_indices:
            if i != j:
                # 重新安置节点
                node = best_route.pop(i)
                best_route.insert(j, node)

                # 计算新路径的总距离
                new_distance = calculate_total_distance([best_route], distances)

                # 更新最优解
                if new_distance < best_distance:
                    best_route = best_route[:]
                    best_distance = new_distance

    return best_route, best_distance

def local_search(routes, distances, iterations=100):
    """
    使用局部搜索算法优化VRP解。

    参数:
    routes (list of lists): 每辆车的初始路径。
    distances (list of dicts): 节点之间的距离数据。
    iterations (int): 最大迭代次数。

    返回:
    tuple: 最优路径和对应的总距离。
    """
    best_routes = [route[:] for route in routes]
    best_distance = calculate_total_distance(best_routes, distances)

    for _ in range(iterations):
        # 使用Swap算子进行路径间优化
        new_routes, new_distance = swap_operator(best_routes, distances)

        if new_distance < best_distance:
            best_routes = new_routes
            best_distance = new_distance

        # 对每条路径使用Relocate算子进行路径内优化
        for i in range(len(best_routes)):
            new_route, new_route_distance = relocate_operator(best_routes[i], distances)
            new_routes = [r[:] if r != best_routes[i] else new_route for r in best_routes]
            new_distance = calculate_total_distance(new_routes, distances)

            if new_distance < best_distance:
                best_routes = new_routes
                best_distance = new_distance

    return best_routes, best_distance

def initialize_routes(nodes, num_vehicles):
    # 车辆路径初始化，保证每辆车都从起点0开始
    routes = [[] for _ in range(num_vehicles)]

    # 将起点0添加到每辆车的路径中
    for i in range(num_vehicles):
        routes[i].append(0)

    # 分配其他节点
    remaining_nodes = nodes[1:]  # 排除起点0
    for index, node in enumerate(remaining_nodes):
        vehicle_index = index % num_vehicles
        routes[vehicle_index].append(node)

    # 确保每辆车都以0结束
    for i in range(num_vehicles):
        if routes[i][-1] != 0:
            routes[i].append(0)

    return routes



# 示例使用
# 假设解析的数据如下
file_path = 'D:/OneDrive - stu.hit.edu.cn/桌面/3L_VRP/code/vrp/by_01.txt'
parsed_data = parse_vrp_file(file_path)

# 初始化解（假设每辆车从0开始到终点）
num_vehicles = parsed_data['general_info']['num_vehicles']-40
nodes = list(range(parsed_data['general_info']['num_customers']))
initial_routes = initialize_routes(nodes, num_vehicles)
print(parsed_data['distances'])
print(initial_routes)
# # 运行局部搜索算法
best_routes, best_distance = local_search(initial_routes, parsed_data['distances'])
print("初始距离",calculate_total_distance(initial_routes,parsed_data['distances']))
print("最优路径:")
for route in best_routes:
    print(route)
print("最优总距离:", best_distance)