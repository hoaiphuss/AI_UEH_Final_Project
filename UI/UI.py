import tkinter as tk
from tkinter import ttk
from knapsack_algorithm import generate_knapsack_problem, knapsack_branch_and_bound_tracking, knapsack_backtracking_tracking
from draw import draw_tree
import time

def show_results():
    try:
        num_items = int(entry_num_items.get())
        if num_items <= 0:
            raise ValueError("Số lượng vật phẩm phải lớn hơn 0.")

        values, weights, capacity = generate_knapsack_problem(num_items)
        result_text.set(
            f"🎯 Giá trị các vật phẩm: {values}\n"
            f"⚖️ Trọng lượng các vật phẩm: {weights}\n"
            f"🧳 Giới hạn trọng lượng túi: {capacity}"
        )

        algo = algorithm_choice.get()
        fitness_tracker = []
        start_time = time.time()

        if algo == "Quay lui cơ bản":
            result = knapsack_backtracking_tracking(weights, values, capacity, len(weights), fitness_tracker=fitness_tracker)
        elif algo == "Nhánh cận":
            solution, max_value, _, fitness_log = knapsack_branch_and_bound_tracking(values, weights, capacity)
            result = {
                "solution": solution,
                "value": max_value,
                "weight": sum(w for i, w in enumerate(weights) if solution[i] == 1)
            }
            fitness_tracker = fitness_log

        elapsed_time = time.time() - start_time
        convergence_speed = sum(
            1 for i in range(1, len(fitness_tracker))
            if fitness_tracker[i] > fitness_tracker[i - 1]
        )

        result_label.config(text=str(result["solution"]))
        total_value_label.config(text=str(result["value"]))
        total_weight_label.config(text=str(result["weight"]))
        time_label.config(text=f"{elapsed_time:.4f}")
        convergence_label.config(text=str(convergence_speed))
        draw_tree(canvas, num_items, values, result["solution"])

        history_table.insert("", "end", values=(
            algo,
            num_items,
            str(result["solution"]),
            result["value"],
            result["weight"],
            f"{elapsed_time:.4f}",
            convergence_speed
        ))

    except ValueError as e:
        result_text.set(f"Lỗi: {e}")

# UI setup
root = tk.Tk()
root.title("🎒 Bài toán Cái Túi - Trình giải trực quan")
root.geometry("1000x750")
root.configure(bg="#f9f9f9")

# ========== FRAME NHẬP LIỆU & KẾT QUẢ ========== #
frame_top = tk.Frame(root, bg="#ffffff", bd=2, relief="groove", padx=10, pady=10)
frame_top.pack(fill=tk.X, padx=15, pady=10)

# Khung trái - Nhập liệu
frame_input = tk.Frame(frame_top, bg="#ffffff")
frame_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

tk.Label(frame_input, text="🔢 Số lượng vật phẩm", font=("Arial", 11), bg="#ffffff").pack(anchor="w", pady=4)
entry_num_items = ttk.Entry(frame_input, width=10)
entry_num_items.pack(anchor="w", pady=4)

tk.Label(frame_input, text="⚙️ Thuật toán", font=("Arial", 11), bg="#ffffff").pack(anchor="w", pady=4)
algorithm_choice = ttk.Combobox(frame_input, values=["Quay lui cơ bản", "Nhánh cận"])
algorithm_choice.current(0)
algorithm_choice.pack(anchor="w", pady=4)

btn_generate = tk.Button(frame_input, text="🚀 Sinh & Giải", font=("Arial", 11, "bold"), bg="#4CAF50", fg="white", padx=10, pady=5, command=show_results)
btn_generate.pack(anchor="w", pady=10)

# Khung phải - Hiển thị kết quả
frame_result = tk.Frame(frame_top, bg="#f1f1f1", bd=1, relief="solid")
frame_result.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

tk.Label(frame_result, text="📊 Kết quả bài toán", font=("Arial", 11, "bold"), bg="#f1f1f1", fg="black").pack(anchor="w", pady=4)
result_text = tk.StringVar()
tk.Label(frame_result, textvariable=result_text, bg="white", font=("Arial", 11), justify="left", wraplength=400).pack(fill=tk.BOTH, expand=True, pady=4, padx=5)

# ========== FRAME THỐNG KÊ TÓM TẮT ========== #
frame_summary = tk.Frame(root, bg="#ffffff", bd=2, relief="groove", padx=10, pady=10)
frame_summary.pack(fill=tk.X, padx=15)

def add_summary_label(title, variable_widget):
    tk.Label(frame_summary, text=title, font=("Arial", 10, "bold"), bg="#ffffff").pack(side=tk.LEFT, padx=10)
    variable_widget.pack(side=tk.LEFT)

result_label = tk.Label(frame_summary, text="0", bg="#ffffff", font=("Arial", 10))
time_label = tk.Label(frame_summary, text="0", bg="#ffffff", font=("Arial", 10))
convergence_label = tk.Label(frame_summary, text="0", bg="#ffffff", font=("Arial", 10))
total_value_label = tk.Label(frame_summary, text="0", bg="#ffffff", font=("Arial", 10))
total_weight_label = tk.Label(frame_summary, text="0", bg="#ffffff", font=("Arial", 10))

add_summary_label("🧮 Giải pháp:", result_label)
add_summary_label("⏱️ Thời gian (s):", time_label)
add_summary_label("📈 Hội tụ:", convergence_label)
add_summary_label("💰 Tổng giá trị:", total_value_label)
add_summary_label("⚖️ Tổng cân nặng:", total_weight_label)

# ========== NOTEBOOK - CÂY & LỊCH SỬ ========== #
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

# Tab Cây trạng thái
tab_tree = tk.Frame(notebook, bg="white")
notebook.add(tab_tree, text="🌲 Cây trạng thái")
canvas = tk.Canvas(tab_tree, bg="white")
canvas.pack(fill=tk.BOTH, expand=True)

# Tab Lịch sử
tab_history = tk.Frame(notebook)
notebook.add(tab_history, text="📜 Lịch sử thí nghiệm")

columns = ("Thuật toán", "Số vật phẩm", "Giải pháp", "Giá trị", "Cân nặng", "Thời gian", "Hội tụ")
history_table = ttk.Treeview(tab_history, columns=columns, show="headings")
for col in columns:
    history_table.heading(col, text=col)
    history_table.column(col, width=120, anchor="center")
history_table.pack(fill=tk.BOTH, expand=True)

root.mainloop()
