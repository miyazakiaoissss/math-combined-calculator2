import streamlit as st
import matplotlib.pyplot as plt
from sympy import sympify, expand
import re

fixed_values = {"a": 3, "b": 2}

def preprocess_expression(expr):
    expr = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expr)
    expr = re.sub(r'(\d)\(', r'\1*(', expr)
    return expr.replace("^", "**")

def regular_triangle(x_center, y_center, size):
    # 正三角形（頂点が上、底辺が下）
    h = size * (3 ** 0.5) / 2
    return [
        (x_center, y_center + h / 2),
        (x_center - size / 2, y_center - h / 2),
        (x_center + size / 2, y_center - h / 2)
    ], h

st.set_page_config(page_title="図形と式の計算", layout="centered")
st.title("図形と式の計算（Streamlit版）")

mode = st.radio("計算の順番を選択してください", ["add_then_mul", "mul_then_add"],
                format_func=lambda x: "四角→三角" if x == "add_then_mul" else "三角→四角")

expr_str = st.text_input("入れる数や式を入力してください（例: 7, 3*a, 2+5）")

fig, ax = plt.subplots(figsize=(7, 1.5))
ax.set_xlim(0, 7)
ax.set_ylim(0, 2)
ax.axis('off')

y = 1.0
rect_w, rect_h = 1.0, 0.8
tri_size = rect_w

if mode == "add_then_mul":
    rect_x = 2.5
    tri_x = 4.5
else:
    tri_x = 2.5
    rect_x = 4.5

input_x = 0.8
result_x = 6.2

# 計算結果と入力表示の初期化
result_display = "0"
input_display = "0"

if expr_str:
    try:
        expr = sympify(preprocess_expression(expr_str))
        a, b = fixed_values["a"], fixed_values["b"]

        if mode == "add_then_mul":
            res = expand((expr + b) * (2 * a))
        else:
            res = expand(expr * a + (-3 * b))

        res_num = res.subs(fixed_values).evalf()
        res_int = int(res_num)
        result_display = str(res_int)

        expr_val = expr.subs(fixed_values).evalf()
        input_display = str(int(expr_val))  # 小数切り捨て必須

    except Exception:
        result_display = "エラー"
        input_display = expr_str

# 入力数字表示（左端）
ax.text(input_x, y, input_display, ha='center', va='center', fontsize=20, fontweight='bold', color="#444")

# 四角形描画
rect = plt.Rectangle((rect_x - rect_w / 2, y - rect_h / 2), rect_w, rect_h,
                     facecolor='lightblue', edgecolor='black', linewidth=2)
ax.add_patch(rect)
rect_label = "b" if mode == "add_then_mul" else "-3b"
ax.text(rect_x, y, rect_label, ha='center', va='center', fontsize=18, fontweight='bold', color="#0D3B66")

# 三角形描画
tri_points, tri_h = regular_triangle(tri_x, y, tri_size)
tri = plt.Polygon(tri_points, closed=True, facecolor='lightgreen', edgecolor='black', linewidth=2)
ax.add_patch(tri)
# 三角形内の文字位置微調整
if mode == "add_then_mul":
    # 2aの文字を三角形の中心より少し右にずらす
    ax.text(tri_x + 0.1, y, "2a", ha='center', va='center', fontsize=18, fontweight='bold', color="#006400")
else:
    ax.text(tri_x, y, "a", ha='center', va='center', fontsize=18, fontweight='bold', color="#006400")

# 矢印描画関数
def draw_arrow(ax, start_x, end_x, y, width=3):
    ax.annotate("", xy=(end_x, y), xytext=(start_x, y),
                arrowprops=dict(arrowstyle="->", linewidth=width, color="#333333"))

# 追加した矢印：図形の左→図形の中心、図形の中心→図形の右
arrow_offset = 0.2
if mode == "add_then_mul":
    # 四角の左→四角の中心
    draw_arrow(ax, rect_x - rect_w / 2 - arrow_offset, rect_x - rect_w / 2 + 0.05, y)
    # 四角の右→三角の左
    draw_arrow(ax, rect_x + rect_w / 2 + 0.05, tri_x - tri_size / 2 - 0.05, y)
    # 三角の右→三角の右端＋offset
    draw_arrow(ax, tri_x + tri_size / 2 + 0.05, tri_x + tri_size / 2 + arrow_offset, y)
else:
    # 三角の左→三角の中心
    draw_arrow(ax, tri_x - tri_size / 2 - arrow_offset, tri_x - tri_size / 2 + 0.05, y)
    # 三角の右→四角の左
    draw_arrow(ax, tri_x + tri_size / 2 + 0.05, rect_x - rect_w / 2 - 0.05, y)
    # 四角の右→四角の右端＋offset
    draw_arrow(ax, rect_x + rect_w / 2 + 0.05, rect_x + rect_w / 2 + arrow_offset, y)

# 結果数字表示（右端）
ax.text(result_x, y, result_display, ha='center', va='center', fontsize=20, fontweight='bold', color="#444")

st.pyplot(fig)
