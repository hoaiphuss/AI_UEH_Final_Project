import random
from queue import PriorityQueue
from typing import List, Tuple

def generate_knapsack_problem(
    num_items: int,
    max_weight: int = 20,
    fill_ratio: float = 0.6,
    seed: int = None
) -> Tuple[List[int], List[int], int]:
    if seed is not None:
        random.seed(seed)
    values = [random.randint(1, 100) for _ in range(num_items)]
    weights = [random.randint(1, max_weight) for _ in range(num_items)]
    capacity = int(sum(weights) * fill_ratio)
    return values, weights, capacity

def knapsack_backtracking_tracking(weights, values, capacity, n, selected=None, best=None, fitness_tracker=None):
    if selected is None:
        selected = [0] * len(weights)
    if best is None:
        best = {"value": 0, "weight": 0, "solution": [0] * len(weights), "branches": 0}
    if fitness_tracker is None:
        fitness_tracker = []

    # Tăng số lượng nhánh được duyệt
    best["branches"] += 1

    # Lưu giá trị tốt nhất hiện tại
    fitness_tracker.append(max(fitness_tracker[-1], best["value"]) if fitness_tracker else best["value"])

    # Điều kiện dừng
    if n == 0 or capacity == 0:
        current_value = sum(values[i] for i in range(len(weights)) if selected[i] == 1)
        current_weight = sum(weights[i] for i in range(len(weights)) if selected[i] == 1)
        if current_value > best["value"]:
            best["value"] = current_value
            best["weight"] = current_weight
            best["solution"] = selected[:]
            
        return best

    # Không chọn vật phẩm thứ n
    selected[n - 1] = 0
    knapsack_backtracking_tracking(weights, values, capacity, n - 1, selected, best, fitness_tracker)

    # Chọn vật phẩm thứ n (nếu có thể)
    if weights[n - 1] <= capacity:
        selected[n - 1] = 1
        knapsack_backtracking_tracking(weights, values, capacity - weights[n - 1], n - 1, selected, best, fitness_tracker)

    return best

class KnapsackNode:
    def __init__(self, level, total_value, total_weight, upper_bound, selected_items):
        self.level = level  # Mức hiện tại trong cây tìm kiếm (ứng với chỉ số vật phẩm)
        self.total_value = total_value  # Tổng giá trị hiện tại
        self.total_weight = total_weight  # Tổng trọng lượng hiện tại
        self.upper_bound = upper_bound  # Cận trên của giá trị tối đa có thể đạt được
        self.selected_items = selected_items  # Danh sách các vật phẩm đã chọn (0/1)

    def __lt__(self, other):
        # Node có cận trên cao hơn được ưu tiên (dùng hàng đợi ưu tiên)
        return self.upper_bound > other.upper_bound

# Hàm tính cận trên của một node
def compute_upper_bound(node, num_items, capacity, values, weights):
    if node.total_weight >= capacity:
        return 0  # Không thể lấy thêm vật phẩm

    bound = node.total_value
    current_weight = node.total_weight

    # Thêm toàn bộ hoặc một phần các vật phẩm còn lại
    for i in range(node.level + 1, num_items):
        if current_weight + weights[i] <= capacity:
            current_weight += weights[i]
            bound += values[i]
        else:
            remain_capacity = capacity - current_weight
            bound += remain_capacity * (values[i] / weights[i])
            break

    return bound

# Thuật toán nhánh và cận với theo dõi hội tụ
def knapsack_branch_and_bound_tracking(values, weights, capacity):
    num_items = len(values)
    priority_queue = PriorityQueue()

    # Sắp xếp vật phẩm theo giá trị trên trọng lượng giảm dần
    items = sorted(zip(values, weights), key=lambda item: item[0] / item[1], reverse=True)
    values, weights = zip(*items)

    # Khởi tạo node gốc
    root = KnapsackNode(
        level=-1,
        total_value=0,
        total_weight=0,
        upper_bound=0,
        selected_items=[0] * num_items
    )
    root.upper_bound = compute_upper_bound(root, num_items, capacity, values, weights)
    priority_queue.put(root)

    best_value = 0
    best_selection = [0] * num_items
    fitness_tracker = []
    nodes_explored = 0

    # Duyệt qua các node trong cây tìm kiếm
    while not priority_queue.empty():
        current_node = priority_queue.get()
        nodes_explored += 1

        # Cập nhật fitness tracker
        last_best = fitness_tracker[-1] if fitness_tracker else 0
        fitness_tracker.append(max(last_best, best_value))

        # Cắt tỉa nếu cận trên không hứa hẹn
        if current_node.upper_bound <= best_value:
            continue

        next_level = current_node.level + 1
        if next_level >= num_items:
            continue

        # Nhánh: chọn vật phẩm ở cấp độ tiếp theo
        left_node = KnapsackNode(
            level=next_level,
            total_value=current_node.total_value + values[next_level],
            total_weight=current_node.total_weight + weights[next_level],
            upper_bound=0,
            selected_items=current_node.selected_items[:]
        )
        left_node.selected_items[next_level] = 1

        if left_node.total_weight <= capacity and left_node.total_value > best_value:
            best_value = left_node.total_value
            best_selection = left_node.selected_items[:]

        left_node.upper_bound = compute_upper_bound(left_node, num_items, capacity, values, weights)
        if left_node.upper_bound > best_value:
            priority_queue.put(left_node)

        # Nhánh: không chọn vật phẩm ở cấp độ tiếp theo
        right_node = KnapsackNode(
            level=next_level,
            total_value=current_node.total_value,
            total_weight=current_node.total_weight,
            upper_bound=0,
            selected_items=current_node.selected_items[:]
        )
        right_node.upper_bound = compute_upper_bound(right_node, num_items, capacity, values, weights)
        if right_node.upper_bound > best_value:
            priority_queue.put(right_node)

    return best_selection, best_value, nodes_explored, fitness_tracker