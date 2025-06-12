import streamlit as st
import matplotlib.pyplot as plt
from sympy import sympify, expand
import re

# 定数
fixed_values = {"a": 3, "b": 2}

def preprocess_expression(expr):
    expr = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expr)
    expr = re.sub(r'(\d)\(', r'\1*(', expr)
    return expr.replace("^", "**")

# 図形描画関数（矢印・三角・四角）
def draw_flow_diagram(mode):
    fig, ax = plt.subplots(figsize=(8, 2))
    y = 0.5
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # 入力
    ax.text(0.5, y, "入力", ha='center', va='center', fontsize=12)

    # 矢印 → 四角 or 三角
    ax.annotate("", xy=(1.4, y), xytext=(0.9, y), arrowprops=dict(arrowstyle="->"))

    if mode == "add_then_mul":
        # 四角（b）
        rect = plt.Rectangle((1.5, y - 0.2), 0.8, 0.4, color='lightblue')
        ax.add_patch(rect)
        ax.text(1.9, y, "b", ha='center', va='center', fontsize=12)

        # 矢印 → 三角
        ax.annotate("", xy=(2.5, y), xytext=(2.3, y), arrowprops=dict(arrowstyle="->"))

        # 三角（2a）※底辺を下に
        triangle = plt.Polygon([[3.3, y + 0.2], [3.7, y + 0.2], [3.5, y - 0.2]], color='lightgreen')
        ax.add_patch(triangle)
        ax.text(3.5, y, "2a", ha='center', va='center', fontsize=12)

        # 矢印 → 出力
        ax.annotate("", xy=(4.3, y), xytext=(4.0, y), arrowprops=dict(arrowstyle="->"))
    else:
        # 三角（a）※底辺を下に
        triangle = plt.Polygon([[1.3, y + 0.2], [1.7, y + 0.2], [1.5, y - 0.2]], color='lightgreen')
        ax.add_patch(triangle)
        ax.text(1.5, y, "a", ha='center', va='center', fontsize=12)

        # 矢印 → 四角
        ax.annotate("", xy=(2.3, y), xytext=(1.9, y), arrowprops=dict(arrowstyle="->"))

        # 四角（-3b）
        rect = plt.Rectangle((2.4, y - 0.2), 0.8, 0.4, color='lightblue')
        ax.add_patch(rect)
        ax.text(2.8, y, "-3b", ha='center', va='center', fontsize=12)

        # 矢印 → 出力
        ax.annotate("", xy=(3.4, y), xytext=(3.2, y), arrowprops=dict(arrowstyle="->"))

    # 出力（右端）
    ax.text(5, y, "出力", ha='left', va='center', fontsize=12)

    return fig

# Streamlit UI
st.set_page_config(page_title="図形と式の計算", layout="centered")
st.title("図形と式の計算（Streamlit版）")

# ラジオボタン：計算の流れの選択
mode = st.radio("計算の順番を選んでください", ["add_then_mul", "mul_then_add"],
                format_func=lambda x: "四角→三角" if x == "add_then_mul" else "三角→四角")

# 入力欄（左にあるべき）
input_col, _, result_col = st.columns([2, 1, 2])

with input_col:
    expr_str = st.text_input("入れる数や式", "")

# 図形と矢印を描く
st.pyplot(draw_flow_diagram(mode))

# 計算処理
if expr_str:
    try:
        expr = sympify(preprocess_expression(expr_str))
        a, b = fixed_values["a"], fixed_values["b"]

        if mode == "add_then_mul":
            res = expand((expr + b) * (2 * a))
        else:
            res = expand(expr * a + (-3 * b))

        res_num = res.subs(fixed_values)

        with result_col:
            st.success(f"→ 結果：{res_num}")
    except Exception as e:
        with result_col:
            st.error("入力に誤りがあります")
