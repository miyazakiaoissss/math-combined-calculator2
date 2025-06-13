import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from sympy import sympify, expand
import re

fixed_values = {"a": 3, "b": 2}

def preprocess_expression(expr):
    expr = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expr)
    expr = re.sub(r'(\d)\(', r'\1*(', expr)
    return expr.replace("^", "**")

def calculate(expr_str, mode):
    expr_str = expr_str.strip()
    if not expr_str:
        return None, "式が入力されていません"

    expr = sympify(preprocess_expression(expr_str))
    a, b = fixed_values["a"], fixed_values["b"]

    if mode == "add_then_mul":
        res = expand((expr + b) * (2 * a))
    else:
        res = expand(expr * a + (-3 * b))

    res_num = res.subs(fixed_values)
    res_num = int(res_num) if res_num == int(res_num) else round(float(res_num), 2)
    return res_num, None

def draw_diagram(mode, input_value, result_value):
    fig, ax = plt.subplots(figsize=(8, 2))
    ax.set_xlim(0, 800)
    ax.set_ylim(0, 200)
    ax.axis('off')

    pos_input = 50
    pos1 = 200
    pos2 = 400
    pos_result = 600
    center_y = 100

    ax.text(pos_input, center_y, str(input_value), fontsize=14, ha='center', va='center')

    if mode == "add_then_mul":
        rect = patches.Rectangle((pos1 - 40, center_y - 30), 80, 60,
                                 linewidth=1.5, edgecolor='black', facecolor='lightblue')
        ax.add_patch(rect)
        ax.text(pos1, center_y, "b", ha='center', va='center', fontsize=14)

        triangle = patches.Polygon([[pos2, center_y + 30],
                                    [pos2 - 50, center_y - 30],
                                    [pos2 + 50, center_y - 30]],
                                   closed=True, facecolor='lightgreen', edgecolor='black', linewidth=1.5)
        ax.add_patch(triangle)
        ax.text(pos2, center_y, "2a", ha='center', va='center', fontsize=14)
    else:
        triangle = patches.Polygon([[pos1, center_y + 30],
                                    [pos1 - 50, center_y - 30],
                                    [pos1 + 50, center_y - 30]],
                                   closed=True, facecolor='lightgreen', edgecolor='black', linewidth=1.5)
        ax.add_patch(triangle)
        ax.text(pos1, center_y, "a", ha='center', va='center', fontsize=14)

        rect = patches.Rectangle((pos2 - 40, center_y - 30), 80, 60,
                                 linewidth=1.5, edgecolor='black', facecolor='lightblue')
        ax.add_patch(rect)
        ax.text(pos2, center_y, "-3b", ha='center', va='center', fontsize=14)

    arrow_props = dict(facecolor='black', shrink=0.05, width=1.2, headwidth=10)
    ax.annotate('', xy=(pos1 - 50, center_y), xytext=(pos_input + 50, center_y), arrowprops=arrow_props)
    ax.annotate('', xy=(pos2 - 50, center_y), xytext=(pos1 + 50, center_y), arrowprops=arrow_props)
    ax.annotate('', xy=(pos_result - 50, center_y), xytext=(pos2 + 50, center_y), arrowprops=arrow_props)

    ax.text(pos_result, center_y, str(result_value), fontsize=14, ha='center', va='center')
    st.pyplot(fig)

# --- Streamlit UI ---

st.title("図形と式の計算")

mode = st.radio("計算の順番", ["add_then_mul", "mul_then_add"],
                format_func=lambda x: "四角形→三角形" if x == "add_then_mul" else "三角形→四角形")

# 横幅を調整するためカラムで分割
col1, col2 = st.columns([1, 1])
with col1:
    st.markdown("**入れる数（整数のみ）**")
with col2:
    input_value = st.number_input(label="", step=1, format="%d", key="input_value", label_visibility="collapsed")

# 入力欄の幅を明示的にCSSで短くする
st.markdown(
    """
    <style>
    section[data-testid="stNumberInput"] input {
        width: 50px !important;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

res, err = calculate(str(input_value), mode)

if err:
    st.error(err)
elif res is not None:
    draw_diagram(mode, input_value, res)
