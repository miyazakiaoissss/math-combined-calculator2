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

# 図形描画関数
def draw_shapes(mode):
    fig, ax = plt.subplots(figsize=(6, 2))
    y = 0.5
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 1)
    ax.axis('off')

    if mode == "add_then_mul":
        # 四角（b）
        rect = plt.Rectangle((1, y - 0.2), 0.8, 0.4, color='lightblue')
        ax.add_patch(rect)
        ax.text(1.4, y, "b", ha='center', va='center', fontsize=12)

        # 三角（2a）
        triangle = plt.Polygon([[3, y - 0.2], [2.6, y + 0.2], [3.4, y + 0.2]], color='lightgreen')
        ax.add_patch(triangle)
        ax.text(3, y, "2a", ha='center', va='center', fontsize=12)

        # 矢印
        ax.annotate("", xy=(0.9, y), xytext=(0.3, y), arrowprops=dict(arrowstyle="->"))
        ax.annotate("", xy=(2.5, y), xytext=(1.9, y), arrowprops=dict(arrowstyle="->"))
        ax.annotate("", xy=(4.5, y), xytext=(3.5, y), arrowprops=dict(arrowstyle="->"))
    else:
        # 三角（a）
        triangle = plt.Polygon([[1.4, y - 0.2], [1, y + 0.2], [1.8, y + 0.2]], color='lightgreen')
        ax.add_patch(triangle)
        ax.text(1.4, y, "a", ha='center', va='center', fontsize=12)

        # 四角（-3b）
        rect = plt.Rectangle((3, y - 0.2), 0.8, 0.4, color='lightblue')
        ax.add_patch(rect)
        ax.text(3.4, y, "-3b", ha='center', va='center', fontsize=12)

        # 矢印
        ax.annotate("", xy=(0.9, y), xytext=(0.3, y), arrowprops=dict(arrowstyle="->"))
        ax.annotate("", xy=(2.8, y), xytext=(2, y), arrowprops=dict(arrowstyle="->"))
        ax.annotate("", xy=(4.8, y), xytext=(3.9, y), arrowprops=dict(arrowstyle="->"))

    return fig

# Streamlit UI
st.title("図形と式の計算（Streamlit版）")

mode = st.radio("計算の順番を選んでください", ["add_then_mul", "mul_then_add"], format_func=lambda x: "四角→三角" if x=="add_then_mul" else "三角→四角")

st.pyplot(draw_shapes(mode))

expr_str = st.text_input("入れる数や式を入力してください", "")

if st.button("計算"):
    if not expr_str:
        st.warning("式を入力してください")
    else:
        try:
            expr = sympify(preprocess_expression(expr_str))
            a, b = fixed_values["a"], fixed_values["b"]

            if mode == "add_then_mul":
                res = expand((expr + b) * (2 * a))
            else:
                res = expand(expr * a + (-3 * b))

            res_num = res.subs(fixed_values)
            st.success(f"結果：{res_num}")
        except Exception as e:
            st.error(f"エラー: {e}")
