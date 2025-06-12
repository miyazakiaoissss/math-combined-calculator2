import streamlit as st
import matplotlib.pyplot as plt
from sympy import sympify, expand
import re

fixed_values = {"a": 3, "b": 2}

def preprocess_expression(expr):
    expr = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expr)
    expr = re.sub(r'(\d)\(', r'\1*(', expr)
    return expr.replace("^", "**")

def regular_triangle(x_center, y_center, side_length):
    # 正三角形の頂点座標（頂点上向き）
    h = side_length * (3 ** 0.5) / 2
    return [
        (x_center, y_center + h / 2),       # 頂点上
        (x_center - side_length / 2, y_center - h / 2),  # 左下
        (x_center + side_length / 2, y_center - h / 2)   # 右下
    ], h

def draw_arrow(ax, start_x, end_x, y, width=3):
    ax.annotate("", xy=(end_x, y), xytext=(start_x, y),
                arrowprops=dict(arrowstyle="->", linewidth=width, color="#333333"))

st.set_page_config(page_title="図形と式の計算", layout="centered")
st.title("図形と式の計算（Streamlit版）")

mode = st.radio("計算の順番を選択してください", ["add_then_mul", "mul_then_add"],
                format_func=lambda x: "四角→三角" if x == "add_then_mul" else "三角→四角")

expr_str = st.text_input("入れる数や式を入力してください（例: 7, 3*a, 2+5）")

fig, ax = plt.subplots(figsize=(9, 2.2))
ax.set_xlim(0, 9)
ax.set_ylim(0, 2.5)
ax.axis('off')

y_center = 1.2  # 図形の縦中心位置

# 三角形の辺の長さを決定（ここから高さを算出）
tri_side = 1.4
tri_points, tri_height = regular_triangle(0, 0, tri_side)

# 四角形の高さを三角形の高さに合わせる
rect_height = tri_height
rect_width = 1.0

# 等間隔配置のためにx座標を決める（左から順に）
# 左端：入力数字
# 1つ目図形
# 矢印1
# 2つ目図形
# 矢印2
# 結果数字（右端）
gap = 1.2  # 図形と矢印の間隔
input_x = 1.0
first_shape_x = input_x + gap
arrow1_start = first_shape_x + rect_width / 2
arrow1_end = arrow1_start + gap * 0.8
second_shape_x = arrow1_end + gap
arrow2_start = second_shape_x + tri_side / 2
arrow2_end = arrow2_start + gap * 0.8
result_x = arrow2_end + gap

# モードによって図形の順番を決定
if mode == "add_then_mul":
    rect_x = first_shape_x
    tri_x = second_shape_x
    rect_label = "b"
    tri_label = "2a"
else:
    tri_x = first_shape_x
    rect_x = second_shape_x
    tri_label = "a"
    rect_label = "-3b"

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
        input_display = str(int(expr_val))  # 小数切り捨て

    except Exception:
        result_display = "エラー"
        input_display = expr_str

# 入力数字表示（左端）
ax.text(input_x, y_center, input_display, ha='center', va='center', fontsize=20, fontweight='bold', color="#444")

# 四角形描画
rect = plt.Rectangle((rect_x - rect_width / 2, y_center - rect_height / 2),
                     rect_width, rect_height,
                     facecolor='lightblue', edgecolor='black', linewidth=2)
ax.add_patch(rect)
ax.text(rect_x, y_center, rect_label, ha='center', va='center', fontsize=18, fontweight='bold', color="#0D3B66")

# 三角形描画
tri_points, tri_height = regular_triangle(tri_x, y_center, tri_side)
tri = plt.Polygon(tri_points, closed=True, facecolor='lightgreen', edgecolor='black', linewidth=2)
ax.add_patch(tri)
ax.text(tri_x, y_center, tri_label, ha='center', va='center', fontsize=18, fontweight='bold', color="#006400")

# 矢印の描画（長さを統一しバランスよく）
draw_arrow(ax, rect_x - rect_width / 2 - gap * 0.6, rect_x - rect_width / 2, y_center)  # 四角の左矢印
draw_arrow(ax, rect_x + rect_width / 2, tri_x - tri_side / 2, y_center)                 # 四角→三角矢印
draw_arrow(ax, tri_x + tri_side / 2, tri_x + tri_side / 2 + gap * 0.6, y_center)       # 三角の右矢印

# 三角→四角モードの場合は矢印を入れ替える
if mode == "mul_then_add":
    draw_arrow(ax, tri_x - tri_side / 2 - gap * 0.6, tri_x - tri_side / 2, y_center)     # 三角の左矢印
    draw_arrow(ax, tri_x + tri_side / 2, rect_x - rect_width / 2, y_center)              # 三角→四角矢印
    draw_arrow(ax, rect_x + rect_width / 2, rect_x + rect_width / 2 + gap * 0.6, y_center)  # 四角の右矢印

# 結果数字表示（右端）
ax.text(result_x, y_center, result_display, ha='center', va='center', fontsize=20, fontweight='bold', color="#444")

st.pyplot(fig)
