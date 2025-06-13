import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from sympy import sympify, expand
import re

# 固定値
a = 3
b = 2

st.set_page_config(layout="wide")
st.title("図形を使った式の計算")

# 入力とモード選択
col_input, col_mode = st.columns([1, 2])
with col_input:
    input_expr = st.number_input("入れる数（整数のみ）", step=1, format="%d")
with col_mode:
    mode = st.radio("計算の順番", ["四角形 → 三角形", "三角形 → 四角形"], horizontal=True)

# 計算処理
def calculate(value):
    if mode == "四角形 → 三角形":
        return (value + b) * (2 * a)
    else:
        return value * a + (-3 * b)

# 描画処理
def draw_diagram(value, result):
    fig, ax = plt.subplots(figsize=(8, 2))
    ax.set_xlim(0, 800)
    ax.set_ylim(0, 200)
    ax.axis('off')

    # 定数
    shape_width = 60
    shape_height = 80
    triangle_height = shape_height
    triangle_width = 80
    spacing = 120
    arrow_len = 40
    text_offset = 10

    # 座標設定
    start_x = 50
    y_center = 100

    if mode == "四角形 → 三角形":
        rect_x = start_x + arrow_len + spacing
        tri_x = rect_x + shape_width + spacing
    else:
        tri_x = start_x + arrow_len + spacing
        rect_x = tri_x + triangle_width + spacing

    output_x = rect_x + shape_width + spacing if mode == "三角形 → 四角形" else tri_x + triangle_width + spacing

    # 入力・出力の数値
    ax.text(start_x, y_center, f"{int(value)}", ha="center", va="center", fontsize=14)
    ax.text(output_x + arrow_len, y_center, f"{int(result)}", ha="center", va="center", fontsize=14)

    # 入力→最初の図形
    ax.annotate("", xy=(rect_x if mode == "四角形 → 三角形" else tri_x, y_center),
                xytext=(start_x + 20, y_center), arrowprops=dict(arrowstyle="->", lw=2))

    # 最初→次の図形
    ax.annotate("", xy=(tri_x if mode == "四角形 → 三角形" else rect_x, y_center),
                xytext=((rect_x + shape_width) if mode == "四角形 → 三角形" else (tri_x + triangle_width), y_center),
                arrowprops=dict(arrowstyle="->", lw=2))

    # 最後→出力
    ax.annotate("", xy=(output_x, y_center),
                xytext=((tri_x + triangle_width) if mode == "四角形 → 三角形" else (rect_x + shape_width), y_center),
                arrowprops=dict(arrowstyle="->", lw=2))

    # 四角形描画
    rect = patches.Rectangle((rect_x, y_center - shape_height/2), shape_width, shape_height,
                             linewidth=2, edgecolor='black', facecolor='lightblue')
    ax.add_patch(rect)
    ax.text(rect_x + shape_width/2, y_center, "b" if mode == "四角形 → 三角形" else "-3b",
            ha="center", va="center", fontsize=14)

    # 三角形描画
    triangle = patches.Polygon(
        [[tri_x + triangle_width/2, y_center - triangle_height/2],
         [tri_x, y_center + triangle_height/2],
         [tri_x + triangle_width, y_center + triangle_height/2]],
        closed=True, edgecolor='black', facecolor='lightgreen', linewidth=2)
    ax.add_patch(triangle)
    ax.text(tri_x + triangle_width/2, y_center + triangle_height * 0.1, "2a" if mode == "四角形 → 三角形" else "a",
            ha="center", va="center", fontsize=14)

    st.pyplot(fig)

# 結果の計算と描画
result = calculate(input_expr)
draw_diagram(input_expr, result)
