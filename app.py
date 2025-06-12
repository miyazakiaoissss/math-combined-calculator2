import tkinter as tk
from sympy import sympify, expand
import re

fixed_values = {"a": 3, "b": 2}

def preprocess_expression(expr):
    expr = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expr)
    expr = re.sub(r'(\d)\(', r'\1*(', expr)
    return expr.replace("^", "**")

def update_layout():
    canvas.delete("all")
    update_canvas_positions()

def update_canvas_positions():
    canvas.delete("all")

    # 図形サイズ（縦は高さで揃える）
    rect_width = 80
    rect_height = 60
    tri_side = 80  # 正三角形の一辺（底辺）
    tri_height = rect_height  # 高さを四角と同じに

    gap = 40  # 図形・矢印・数字の間の最小スペース（px）

    # Y座標は全要素の中心を合わせる
    center_y = 100

    # 入力数字のX座標（左端より少し内側に）
    input_x = 60

    rect_half_w = rect_width / 2
    tri_half_w = tri_side / 2

    # モードによって図形の順序を設定
    if mode.get() == "add_then_mul":
        # 順序: 入力 → 四角形 → 三角形 → 結果
        first_shape = "rect"
        second_shape = "tri"
    else:
        # 順序: 入力 → 三角形 → 四角形 → 結果
        first_shape = "tri"
        second_shape = "rect"

    # X座標配置
    # 入力_xは固定
    # 図形は均等間隔で配置するため、全体幅を計算して配置
    total_width = rect_width + tri_side + gap * 4 + 100  # 余裕を持たせる

    # それぞれのX座標を計算
    first_x = input_x + 50 + gap  # 入力から少し離す
    second_x = first_x + (rect_width if first_shape == "rect" else tri_side) + gap
    result_x = second_x + (rect_width if second_shape == "rect" else tri_side) + gap + 40  # 結果はさらに離す

    # 矢印の始点・終点座標
    # 入力 → first_shape
    arrow1_start = input_x + 15
    arrow1_end = first_x - (rect_half_w if first_shape == "rect" else tri_half_w) - 5

    # first_shape → second_shape
    arrow2_start = first_x + (rect_half_w if first_shape == "rect" else tri_half_w) + 5
    arrow2_end = second_x - (rect_half_w if second_shape == "rect" else tri_half_w) - 5

    # second_shape → 結果
    arrow3_start = second_x + (rect_half_w if second_shape == "rect" else tri_half_w) + 5
    arrow3_end = result_x - 15

    # 入力数字表示（整数のみ許可）
    try:
        val = int(entry_input.get())
        input_text = str(val)
    except:
        input_text = ""

    # 図形描画関数
    def draw_rectangle(x, y, text):
        canvas.create_rectangle(x - rect_half_w, y - rect_height/2,
                                x + rect_half_w, y + rect_height/2,
                                fill="lightblue")
        canvas.create_text(x, y, text=text, font=("Arial", 16))

    def draw_triangle(x, y, text):
        top = y - tri_height / 2
        left = x - tri_half_w
        right = x + tri_half_w
        bottom = y + tri_height / 2
        canvas.create_polygon(
            left, bottom,
            right, bottom,
            x, top,
            fill="lightgreen"
        )
        canvas.create_text(x, y, text=text, font=("Arial", 16))

    # 図形描画
    if first_shape == "rect":
        draw_rectangle(first_x, center_y, "b")
    else:
        draw_triangle(first_x, center_y, "2a")

    if second_shape == "rect":
        draw_rectangle(second_x, center_y, "-3b")
    else:
        draw_triangle(second_x, center_y, "a")

    # 矢印描画（すべて左から右）
    canvas.create_line(arrow1_start, center_y, arrow1_end, center_y,
                       arrow=tk.LAST, width=2)
    canvas.create_line(arrow2_start, center_y, arrow2_end, center_y,
                       arrow=tk.LAST, width=2)
    canvas.create_line(arrow3_start, center_y, arrow3_end, center_y,
                       arrow=tk.LAST, width=2)

    # 入力数表示（左端）
    canvas.create_text(input_x, center_y, text=input_text, font=("Arial", 16))

    # 計算結果（整数のみ表示）
    try:
        expr_val = int(entry_input.get())
        expr = sympify(expr_val)
        a, b = fixed_values["a"], fixed_values["b"]

        if mode.get() == "add_then_mul":
            res = expand((expr + b) * (2 * a))
        else:
            res = expand(expr * a + (-3 * b))

        res_val = int(res.evalf())
        canvas.create_text(result_x, center_y, text=str(res_val), font=("Arial", 16))
    except Exception:
        canvas.create_text(result_x, center_y, text="エラー", font=("Arial", 16))

# GUIセットアップ
window = tk.Tk()
window.title("図形と式の計算（矢印左→右修正版）")
window.geometry("720x250")

# 入力欄はキャンバス上部に独立
input_frame = tk.Frame(window)
tk.Label(input_frame, text="入れる数（整数のみ）:").pack(side="left")
entry_input = tk.Entry(input_frame, width=10)
entry_input.pack(side="left")
input_frame.pack(pady=10)

mode = tk.StringVar(value="add_then_mul")
mode_frame = tk.Frame(window)
tk.Label(mode_frame, text="計算の順番：").pack(side="left")
tk.Radiobutton(mode_frame, text="四角→三角", variable=mode, value="add_then_mul", command=update_layout).pack(side="left")
tk.Radiobutton(mode_frame, text="三角→四角", variable=mode, value="mul_then_add", command=update_layout).pack(side="left")
mode_frame.pack()

tk.Button(window, text="計算", command=update_layout).pack(pady=5)

canvas = tk.Canvas(window, width=700, height=200, bg="white")
canvas.pack(pady=10)

window.mainloop()
