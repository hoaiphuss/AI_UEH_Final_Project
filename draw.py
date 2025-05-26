import tkinter as tk

def draw_node(canvas: tk.Canvas, x: int, y: int, text: str, is_selected: bool, parent_selected: bool):
    """Vẽ một nút với màu sắc tùy theo trạng thái lựa chọn"""
    if is_selected and parent_selected:
        color = "lightgreen"
    elif is_selected:
        color = "lightblue"
    else:
        color = "lightgray"
    canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill=color, outline="black")
    canvas.create_text(x, y, text=text)

def draw_branch(canvas: tk.Canvas, x: int, y: int, dx: int, dy: int, text: str, 
                current_value: int, is_selected: bool, parent_selected: bool, 
                remaining_items: int, level: int, level_height: int, 
                node_radius: int, values: list, selected: list, h_spacing: int, 
                pass_selection: bool):
    """Vẽ một nhánh con của cây"""
    new_x = x + dx
    new_y = y + dy
    draw_node(canvas, new_x, new_y, text, is_selected, parent_selected)
    canvas.create_line(x, y + node_radius, new_x, new_y - node_radius)

    # Chỉ gọi lại hàm draw_subtree nếu vẫn còn vật phẩm để chọn
    if remaining_items > 1:
        draw_subtree(canvas, new_x, new_y, remaining_items - 1, level + 1, 
                     level_height, node_radius, values, selected, h_spacing // 2, pass_selection)

def draw_subtree(canvas: tk.Canvas, x: int, y: int, remaining_items: int, level: int, 
                 level_height: int, node_radius: int, values: list, selected: list, 
                 h_spacing: int, parent_selected: bool):
    """Vẽ cây nhị phân đệ quy"""
    if remaining_items == 0:
        return

    idx = len(values) - remaining_items
    current_value = values[idx]
    is_selected = selected[idx] == 1

    next_y = y + level_height

    # Nhánh trái: chọn
    draw_branch(canvas, x, y, -h_spacing, level_height, f"{current_value}", current_value,
                is_selected, parent_selected, remaining_items, level, level_height, node_radius,
                values, selected, h_spacing, is_selected if parent_selected else False)

    # Nhánh phải: không chọn
    draw_branch(canvas, x, y, h_spacing, level_height, "0", current_value,
                not is_selected, parent_selected, remaining_items, level, level_height, node_radius,
                values, selected, h_spacing, not is_selected if parent_selected else False)

def draw_tree(canvas: tk.Canvas, num_items: int, values: list, selected: list):
    """Vẽ toàn bộ cây"""
    canvas.delete("all")
    if num_items == 0:
        return

    canvas_width = 1500
    x = canvas_width // 2
    y = 50
    level_height = 80
    node_radius = 20
    h_spacing = canvas_width // 4

    draw_node(canvas, x, y, "Start", is_selected=True, parent_selected=True)
    draw_subtree(canvas, x, y, num_items, 1, level_height, node_radius, values, selected, h_spacing, parent_selected=True)