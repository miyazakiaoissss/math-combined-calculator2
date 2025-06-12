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
    global text_output

    canvas.delete("all")

    # 図形サイズ（縦は高さで揃える）
    rect_width = 80
    rect_height = 60
    tri_side = 80  # 正三角形の一辺（底辺）
    tri_height = rect_height  # 高さを四角と同じに

    gap = 40  # 図形・矢印・数字の間の最小スペース（px）

    # キャンバス横幅
    canvas_width = 640

    # 入力数字のX座標（左端より少し内側に）
    input_x = 60

    # 図形のX座標（左から順に配置）
    # 四角形と三角形の幅は半分ずつ考慮して間隔を空ける
    # 入力数字 → 四角or三角 → 矢印 → 三角or四角 → 矢印 → 結果数字
    # modeによって並び順変わるので分岐

    # 半幅
    rect_half_w = rect_width / 2
    tri_half_w = tri_side / 2

    # Y座標は全要素の中心を合わせる
    center_y = 100

    if mode.get() == "add_then_mul":
        # 四角形→三角形の順
        rect_x = input_x + rect_half_w + gap
        tri_x = rect_x + rect_half_w + tri_half_w + gap
    else:
        # 三角形→四角形の順
        tri_x = input_x + tri_half_w + gap
        rect_x = tri_x + tri_half_w + rect_half_w + gap

    # 矢印の座標（始点・終点）
    arrow1_start = input_x + 15  # 入力数字→図形左端の矢印少し内側スタート
    arrow1_end = (rect_x if mode.get() == "add_then_mul" else tri_x) - (rect_half_w if mode.get() == "add_then_mul" else tri_half_w) - 5

    arrow2_start = (rect_x if mode.get() == "add_then_mul" else tri_x) + (rect_half_w if mode.get() == "add_then_mul" else tri_half_w) + 5
    arrow2_end = (tri_x if mode.get() == "add_then_mul" else rect_x) - (tri_half_w if mode.get() == "add_then_mul" else rect_half_w) - 5

    arrow3_start = (tri_x if mode.get() == "add_then_mul" else rect_x) + (tri_half_w if mode.get() == "add_then_mul" else rect_half_w) + 5
    result_x = arrow3_start + gap

    # 入力数字（整数のみ許可）表示は左に
    try:
        val = int(entry_input.get())
        input_text = str(val)
    except:
        input_text = ""

    # 図形描画
    # 四角形
    canvas.create_rectangle(rect_x - rect_half_w, center_y - rect_height/2,
                            rect_x + rect_half_w, center_y + rect_height/2,
                            fill="lightblue")
    # 四角形内の文字
    rect_text = "b" if mode.get() == "add_then_mul" else "-3b"
    canvas.create_text(rect_x, center_y, text=rect_text, font=("Arial", 16))

    # 三角形（正三角形で底辺が下、中心を(x,y)に）
    # 頂点の3点座標計算
    tri_top = center_y - tri_height / 2
    tri_left = tri_x - tri_half_w
    tri_right = tri_x + tri_half_w
    tri_bottom = center_y + tri_height / 2

    canvas.create_polygon(
        tri_left, tri_bottom,  # 左下
        tri_right, tri_bottom, # 右下
        tri_x, tri_top,        # 上頂点
        fill="lightgreen"
    )
    tri_text = "2a" if mode.get() == "add_then_mul" else "a"
    canvas.create_text(tri_x, center_y, text=tri_text, font=("Arial", 16))

    # 矢印を3本描画（左右矢印も追加）
    # 左端（入力→図形）
    canvas.create_line(input_x + 15, center_y, arrow1_end, center_y,
                       arrow=tk.LAST, width=2)
    # 図形間
    canvas.create_line(arrow2_start, center_y, arrow2_end, center_y,
                       arrow=tk.LAST, width=2)
    # 図形→結果数字
    canvas.create_line(arrow3_start, center_y, result_x - 10, center_y,
                       arrow=tk.LAST, width=2)

    # 入力数表示（図形左の少し左）
    canvas.create_text(input_x, center_y, text=input_text, font=("Arial", 16))

    # 結果計算＆表示（整数のみ）
    try:
        expr_val = int(entry_input.get())
        expr = sympify(expr_val)
        a, b = fixed_values["a"], fixed_values["b"]

        if mode.get() == "add_then_mul":
            res = expand((expr + b) * (2 * a))
        else:
            res = expand(expr * a + (-3 * b))

        # 結果を整数に丸めて表示
        res_val = int(res.evalf())
        canvas.create_text(result_x, center_y, text=str(res_val), font=("Arial", 16))
    except Exception as e:
        canvas.create_text(result_x, center_y, text="エラー", font=("Arial", 16))

# ウィンドウセットアップ
window = tk.Tk()
window.title("図形と式の計算（横バランス調整済み）")
window.geometry("700x250")

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

canvas = tk.Canvas(window, width=640, height=200, bg="white")
canvas.pack(pady=10)

window.mainloop()
