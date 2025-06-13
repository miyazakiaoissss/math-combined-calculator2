import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from sympy import sympify, expand
import re

# 定数設定
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

    # 四角と三角の位置
    pos_input = 50
    pos1 = 200
    pos2 = 400
    pos_result = 600
    center_y = 100

    # 入力値
    ax.text(pos_input, center_y, str(input_value), fontsize=14, ha='center', va='center')

    # 図形と処理式
    if mode == "add_then_mul":
        # 四角形
        rect = patches.Rectangle((pos1 - 40, center_y - 30), 80, 60, linewidth=1, edgecolor='black', facecolor='lightblue')
        ax.add_patch(rect)
        ax.text(pos1, center_y, "b", ha='center', va='center', fontsize=14)

        # 三角形（正三角形で高さ＝四角の高さ）
        triangle_height = 60
        half_base = 50
        triangle = patches.Polygon([[pos2, center_y + triangle_height/2],
                                    [pos2 - half_base, center_y - triangle_height/2],
                                    [pos2 + half_base, center_y - triangle_height/2]],
                                    closed=True, color='lightgreen')
        ax.add_patch(triangle)
        ax.text(pos2, center_y, "2a", ha='center', va='center', fontsize=14)
    else:
        # 三角形
        triangle_height = 60
        half_base = 50
        triangle = patches.Polygon([[pos1, center_y + triangle_height/2],
                                    [pos1 - half_base, center_y - triangle_height/2],
                                    [pos1 + half_base, center_y - triangle_height/2]],
                                    closed=True, color='lightgreen')
        ax.add_patch(triangle)
        ax.text(pos1, center_y, "a", ha='center', va='center', fontsize=14)

        # 四角形
        rect = patches.Rectangle((pos2 - 40, center_y - 30), 80, 60, linewidth=1, edgecolor='black', facecolor='lightblue')
        ax.add_patch(rect)
        ax.text(pos2, center_y, "-3b", ha='center', va='center', fontsize=14)

    # 矢印
    arrow_props = dict(facecolor='black', shrink=0.05, width=1, headwidth=10)
    ax.annotate('', xy=(pos1 - 60, center_y), xytext=(pos_input + 30, center_y), arrowprops=arrow_props)
    ax.annotate('', xy=(pos2 - 60, center_y), xytext=(pos1 + 60, center_y), arrowprops=arrow_props)
    ax.annotate('', xy=(pos_result - 30, center_y), xytext=(pos2 + 60, center_y), arrowprops=arrow_props)

    # 結果
    ax.text(pos_result, center_y, str(result_value), fontsize=14, ha='center', va='center')

    st.pyplot(fig)

# --- Streamlit UI ---

st.title("図形と式の計算")

# モード選択
mode = st.radio("計算の順番", ["add_then_mul", "mul_then_add"], format_func=lambda x: "四角→三角" if x == "add_then_mul" else "三角→四角")

# 入力
input_value = st.number_input("入れる数（整数のみ）", step=1, format="%d")

# 計算
res, err = calculate(str(input_value), mode)

# 描画
if err:
    st.error(err)
elif res is not None:
    draw_diagram(mode, input_value, res)
