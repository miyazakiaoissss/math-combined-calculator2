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
    h = size * (3 ** 0.5) / 2
    return [
        (x_center, y_center + h/2),
        (x_center - size/2, y_center - h/2),
        (x_center + size/2, y_center - h/2)
    ], h

def draw_flow_diagram(mode):
    fig, ax = plt.subplots(figsize=(6, 2))
    ax.set_xlim(1.5, 5.5)
    ax.set_ylim(0, 2)
    ax.axis('off')

    # 高さをすべて1.0に揃える
    y = 1.0
    rect_width = 0.8
    tri_size = 0.8 / (3 ** 0.5 / 2)

    if mode == "add_then_mul":
        # 四角形（高さ0.8、中心y=1.0）
        rect = plt.Rectangle((2.0, y - 0.4), rect_width, 0.8, color='lightblue', ec="black", lw=1.5)
        ax.add_patch(rect)
        ax.text(2.0 + rect_width/2, y, "b", ha='center', va='center', fontsize=14, fontweight='bold', color="#0D3B66")

        ax.annotate("", xy=(2.85, y), xytext=(2.75, y), arrowprops=dict(arrowstyle="->", lw=1.5, color="#333333"))
        ax.text(2.8, y, "", ha='center', va='center')  # 矢印ラベルはなし（空テキスト）

        # 三角形
        triangle_points, tri_h = regular_triangle(3.5, y, tri_size)
        triangle = plt.Polygon(triangle_points, color='lightgreen', ec="black", lw=1.5)
        ax.add_patch(triangle)
        ax.text(3.5, y, "2a", ha='center', va='center', fontsize=14, fontweight='bold', color="#006400")

        ax.annotate("", xy=(4.15, y), xytext=(4.0, y), arrowprops=dict(arrowstyle="->", lw=1.5, color="#333333"))
        ax.text(4.1, y, "", ha='center', va='center')

    else:
        # 三角形
        triangle_points, tri_h = regular_triangle(2.1, y, tri_size)
        triangle = plt.Polygon(triangle_points, color='lightgreen', ec="black", lw=1.5)
        ax.add_patch(triangle)
        ax.text(2.1, y, "a", ha='center', va='center', fontsize=14, fontweight='bold', color="#006400")

        ax.annotate("", xy=(2.75, y), xytext=(2.4, y), arrowprops=dict(arrowstyle="->", lw=1.5, color="#333333"))
        ax.text(2.6, y, "", ha='center', va='center')

        # 四角形
        rect = plt.Rectangle((3.0, y - 0.4), rect_width, 0.8, color='lightblue', ec="black", lw=1.5)
        ax.add_patch(rect)
        ax.text(3.0 + rect_width/2, y, "-3b", ha='center', va='center', fontsize=14, fontweight='bold', color="#0D3B66")

        ax.annotate("", xy=(3.75, y), xytext=(3.4, y), arrowprops=dict(arrowstyle="->", lw=1.5, color="#333333"))
        ax.text(3.6, y, "", ha='center', va='center')

    return fig

st.set_page_config(page_title="図形と式の計算", layout="centered")
st.title("図形と式の計算（Streamlit版）")

mode = st.radio("計算の順番を選んでください", ["add_then_mul", "mul_then_add"],
                format_func=lambda x: "四角→三角" if x == "add_then_mul" else "三角→四角")

input_col, _, center_col, _, right_col = st.columns([1.5, 0.2, 4, 0.2, 1.5])

with input_col:
    expr_str = st.text_input("入れる数や式", "")

with center_col:
    st.pyplot(draw_flow_diagram(mode))

with right_col:
    if expr_str:
        try:
            expr = sympify(preprocess_expression(expr_str))
            a, b = fixed_values["a"], fixed_values["b"]

            if mode == "add_then_mul":
                res = expand((expr + b) * (2 * a))
            else:
                res = expand(expr * a + (-3 * b))

            res_num = res.subs(fixed_values).evalf()

            # 結果は整数で表示
            display_val = str(int(res_num))

            st.markdown(f"<div style='display:flex;align-items:center;height:40px;font-size:20px;font-weight:bold;color:#111;'>{display_val}</div>", unsafe_allow_html=True)
        except Exception:
            st.error("入力に誤りがあります")
