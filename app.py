import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from sympy import sympify, expand
import re

fixed_values = {"a": 3, "b": 2}

st.set_page_config(layout="wide")
st.title("図形と式の計算")

# 入力
input_expr = st.number_input("入れる数", step=1, format="%d")
mode = st.radio("計算の順番", ("四角形→三角形", "三角形→四角形"), horizontal=True)

# 前処理（数式の整形）
def preprocess_expression(expr):
    expr = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', str(expr))
    expr = re.sub(r'(\d)\(', r'\1*(', expr)
    return expr.replace("^", "**")

# 計算
expr = sympify(preprocess_expression(str(input_expr)))
a, b = fixed_values["a"], fixed_values["b"]

if mode == "四角形→三角形":
    res_expr = expand((expr + b) * (2 * a))
else:
    res_expr = expand(expr * a + (-3 * b))

res_num = int(res_expr.evalf())

# 描画
def draw_diagram():
    fig, ax = plt.subplots(figsize=(8, 2))
    ax.set_xlim(0, 800)
    ax.set_ylim(0, 200)
    ax.axis('off')

    y_center = 100
    arrow_y = y_center
    shape_width = 80
    shape_height = 80
    arrow_length = 60
    gap = 20

    if mode == "四角形→三角形":
        # 入力
        ax.text(40, y_center, f"{int(input_expr)}", fontsize=14, va="center", ha="center")
        ax.annotate('', xy=(70, arrow_y), xytext=(55, arrow_y), arrowprops=dict(arrowstyle='->', lw=2))

        # 四角形
        rect_x = 70 + gap
        rect = patches.Rectangle((rect_x, y_center - shape_height/2), shape_width, shape_height,
                                 linewidth=2, edgecolor='black', facecolor='lightblue')
        ax.add_patch(rect)
        ax.text(rect_x + shape_width/2, y_center, "b", fontsize=14, va="center", ha="center")

        ax.annotate('', xy=(rect_x + shape_width + gap, arrow_y),
                    xytext=(rect_x + shape_width, arrow_y), arrowprops=dict(arrowstyle='->', lw=2))

        # 三角形
        tri_x = rect_x + shape_width + gap + gap
        triangle = patches.Polygon([
            (tri_x, y_center + shape_height/2),
            (tri_x + shape_width/2, y_center - shape_height/2),
            (tri_x + shape_width, y_center + shape_height/2)
        ], closed=True, edgecolor='black', facecolor='lightgreen', linewidth=2)
        ax.add_patch(triangle)
        ax.text(tri_x + shape_width/2, y_center + 10, "2a", fontsize=14, va="center", ha="center")

        ax.annotate('', xy=(tri_x + shape_width + gap, arrow_y),
                    xytext=(tri_x + shape_width, arrow_y), arrowprops=dict(arrowstyle='->', lw=2))

        # 出力
        ax.text(tri_x + shape_width + gap + 25, y_center, f"{res_num}", fontsize=14, va="center", ha="center")

    else:
        # 入力
        ax.text(40, y_center, f"{int(input_expr)}", fontsize=14, va="center", ha="center")
        ax.annotate('', xy=(70, arrow_y), xytext=(55, arrow_y), arrowprops=dict(arrowstyle='->', lw=2))

        # 三角形
        tri_x = 70 + gap
        triangle = patches.Polygon([
            (tri_x, y_center + shape_height/2),
            (tri_x + shape_width/2, y_center - shape_height/2),
            (tri_x + shape_width, y_center + shape_height/2)
        ], closed=True, edgecolor='black', facecolor='lightgreen', linewidth=2)
        ax.add_patch(triangle)
        ax.text(tri_x + shape_width/2, y_center + 10, "a", fontsize=14, va="center", ha="center")

        ax.annotate('', xy=(tri_x + shape_width + gap, arrow_y),
                    xytext=(tri_x + shape_width, arrow_y), arrowprops=dict(arrowstyle='->', lw=2))

        # 四角形
        rect_x = tri_x + shape_width + gap + gap
        rect = patches.Rectangle((rect_x, y_center - shape_height/2), shape_width, shape_height,
                                 linewidth=2, edgecolor='black', facecolor='lightblue')
        ax.add_patch(rect)
        ax.text(rect_x + shape_width/2, y_center, "-3b", fontsize=14, va="center", ha="center")

        ax.annotate('', xy=(rect_x + shape_width + gap, arrow_y),
                    xytext=(rect_x + shape_width, arrow_y), arrowprops=dict(arrowstyle='->', lw=2))

        # 出力
        ax.text(rect_x + shape_width + gap + 25, y_center, f"{res_num}", fontsize=14, va="center", ha="center")

    st.pyplot(fig)

draw_diagram()
