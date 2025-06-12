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
        (x_center, y_center + h / 3),
        (x_center - size / 2, y_center - h * 2 / 3),
        (x_center + size / 2, y_center - h * 2 / 3)
    ]

def draw_flow_diagram(mode):
    fig, ax = plt.subplots(figsize=(6, 2))
    ax.set_xlim(1.5, 5.5)
    ax.set_ylim(0, 2)
    ax.axis('off')

    y = 1.0
    shape_size = 1.0

    # 四角と三角の位置
    if mode == "add_then_mul":
        # 四角
        rect = plt.Rectangle((2.0, y - 0.3), 0.6, 0.6, color='lightblue')
        ax.add_patch(rect)
        ax.text(2.3, y, "b", ha='center', va='center', fontsize=12)

        # 矢印
        ax.annotate("", xy=(2.7, y), xytext=(2.6, y), arrowprops=dict(arrowstyle="->"))

        # 三角
        triangle = plt.Polygon(regular_triangle(3.3, y, shape_size), color='lightgreen')
        ax.add_patch(triangle)
        ax.text(3.3, y, "2a", ha='center', va='center', fontsize=12)

        # 矢印
        ax.annotate("", xy=(3.9, y), xytext=(3.7, y), arrowprops=dict(arrowstyle="->"))

    else:
        # 三角
        triangle = plt.Polygon(regular_triangle(2.1, y, shape_size), color='lightgreen')
        ax.add_patch(triangle)
        ax.text(2.1, y, "a", ha='center', va='center', fontsize=12)

        # 矢印
        ax.annotate("", xy=(2.7, y), xytext=(2.4, y), arrowprops=dict(arrowstyle="->"))

        # 四角
        rect = plt.Rectangle((3.0, y - 0.3), 0.6, 0.6, color='lightblue')
        ax.add_patch(rect)
        ax.text(3.3, y, "-3b", ha='center', va='center', fontsize=12)

        # 矢印
        ax.annotate("", xy=(3.6, y), xytext=(3.4, y), arrowprops=dict(arrowstyle="->"))

    return fig

st.set_page_config(page_title="図形と式の計算", layout="centered")
st.title("図形と式の計算（Streamlit版）")

mode = st.radio("計算の順番を選んでください", ["add_then_mul", "mul_then_add"],
                format_func=lambda x: "四角→三角" if x == "add_then_mul" else "三角→四角")

input_col, _ = st.columns([2, 5])
with input_col:
    expr_str = st.text_input("入れる数や式", "")

# 図形と「入れる数」「結果」の横並び表示用カラム
left_col, center_col, right_col = st.columns([1, 3, 1])

with center_col:
    st.pyplot(draw_flow_diagram(mode))

with left_col:
    if expr_str:
        st.markdown(f"**入れる数**")
        st.write(expr_str)

with right_col:
    if expr_str:
        try:
            expr = sympify(preprocess_expression(expr_str))
            a, b = fixed_values["a"], fixed_values["b"]

            if mode == "add_then_mul":
                res = expand((expr + b) * (2 * a))
            else:
                res = expand(expr * a + (-3 * b))

            res_num = res.subs(fixed_values)

            st.markdown(f"**結果**")
            st.success(f"{res_num}")
        except Exception:
            st.error("入力に誤りがあります")
